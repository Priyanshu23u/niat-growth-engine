// Automated HTTP API Integration Test for NIAT ParentTrust AI
const http = require("http");
const app = require("./server/index.js");

const TEST_PORT = 3099;
let server;

function request(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const dataString = body ? JSON.stringify(body) : null;
    const req = http.request(
      {
        hostname: "127.0.0.1",
        port: TEST_PORT,
        path,
        method,
        headers: {
          "Content-Type": "application/json",
          ...(dataString ? { "Content-Length": Buffer.byteLength(dataString) } : {}),
        },
      },
      (res) => {
        let rawData = "";
        res.on("data", (chunk) => (rawData += chunk));
        res.on("end", () => {
          try {
            resolve({
              statusCode: res.statusCode,
              headers: res.headers,
              body: res.headers["content-type"]?.includes("application/json")
                ? JSON.parse(rawData)
                : rawData,
            });
          } catch (e) {
            resolve({ statusCode: res.statusCode, body: rawData });
          }
        });
      }
    );
    req.on("error", reject);
    if (dataString) req.write(dataString);
    req.end();
  });
}

async function runApiTests() {
  console.log("=== RUNNING LIVE HTTP API INTEGRATION TESTS ===");
  let passed = 0;
  let failed = 0;

  function assert(condition, message) {
    if (condition) {
      console.log(`✓ PASS: ${message}`);
      passed++;
    } else {
      console.error(`✗ FAIL: ${message}`);
      failed++;
    }
  }

  server = app.listen(TEST_PORT, async () => {
    try {
      // 1. Test GET /api/health
      const healthRes = await request("GET", "/api/health");
      assert(healthRes.statusCode === 200, "GET /api/health returns 200 OK");
      assert(healthRes.body.status === "healthy", "Health check reports 'healthy'");
      assert(healthRes.body.frontendTechnology.includes("HTML5"), "Reports plain HTML5 frontend");

      // 2. Test GET /api/campuses
      const campusesRes = await request("GET", "/api/campuses?state=Telangana");
      assert(campusesRes.statusCode === 200, "GET /api/campuses returns 200 OK");
      assert(campusesRes.body.success === true, "Campuses query success is true");
      assert(campusesRes.body.campuses.length >= 2, `Returned ${campusesRes.body.campuses.length} Telangana campuses`);

      // 3. Test POST /api/roi
      const roiRes = await request("POST", "/api/roi", {
        niatTotalFee: 1200000,
        tier3TotalFee: 400000,
        niatExpectedStartingSalary: 850000,
        tier3ExpectedStartingSalary: 360000,
      });
      assert(roiRes.statusCode === 200, "POST /api/roi returns 200 OK");
      assert(roiRes.body.metrics.breakEvenMonths > 0, `Break-even computed: ${roiRes.body.metrics.breakEvenMonths} months`);
      assert(roiRes.body.yearlyProjections.length === 5, "ROI returns 5-year projections");

      // 4. Test GET /api/roi
      const defaultRoiRes = await request("GET", "/api/roi");
      assert(defaultRoiRes.statusCode === 200, "GET /api/roi returns 200 OK");
      assert(defaultRoiRes.body.metrics.breakEvenMonths > 0, "Default ROI returns valid metrics");

      // 5. Test POST /api/agent (Telugu inquiry)
      const agentRes = await request("POST", "/api/agent", {
        prompt: "ఈ డిగ్రీ నిజంగా యూజీసీ గుర్తింపు పొందినదేనా?",
        language: "te",
        objectionCategory: "accreditation",
        studentProfile: {
          name: "Sai Teja",
          parentName: "Venkatesh",
          boardPercentage: 88,
          natScore: 82,
          state: "Telangana",
          budgetAnnual: 300000,
        },
      });
      assert(agentRes.statusCode === 200, "POST /api/agent returns 200 OK");
      assert(agentRes.body.success === true, "Agent execution returned success");
      assert(agentRes.body.executedTools.length >= 4, `Agent executed ${agentRes.body.executedTools.length} tools`);
      assert(agentRes.body.agentResponse.includes("గౌరవనీయులైన"), "Agent responded in authentic respectful Telugu");
      assert(agentRes.body.dossierData.dossierId.startsWith("NIAT-DOSSIER-"), `Generated valid dossier ID: ${agentRes.body.dossierData.dossierId}`);

      // 6. Test GET /api/leads
      const leadsRes = await request("GET", "/api/leads");
      assert(leadsRes.statusCode === 200, "GET /api/leads returns 200 OK");
      assert(leadsRes.body.leads.length >= 5, `Pipeline holds ${leadsRes.body.leads.length} leads`);
      assert(leadsRes.body.analytics.funnelComparison !== undefined, "Telemetry includes A/B funnel comparison");

      // 7. Test POST /api/leads
      const newLeadRes = await request("POST", "/api/leads", {
        studentName: "Meera Nair",
        parentName: "G. Nair",
        parentPhone: "+91 94471 22334",
        language: "ml",
        boardPercentage: 90,
        natScore: 85,
        state: "Kerala",
        budgetAnnual: 310000,
        seatReserved: false,
      });
      assert(newLeadRes.statusCode === 200, "POST /api/leads returns 200 OK");
      assert(newLeadRes.body.lead.studentName === "Meera Nair", "Recorded new student lead successfully");

      // 8. Test POST /api/reserve-seat
      const seatRes = await request("POST", "/api/reserve-seat", {
        studentName: "Sai Teja",
        parentName: "Venkatesh",
        parentPhone: "+91 98480 23456",
        campusId: "campus-chaitanya-hyd",
        campusName: "NIAT @ Chaitanya",
      });
      assert(seatRes.statusCode === 200, "POST /api/reserve-seat returns 200 OK");
      assert(seatRes.body.reservation.status === "PROVISIONAL_CONFIRMED", "Provisional seat confirmed");
      assert(seatRes.body.reservation.tokenAmount === 10000, "Token amount is ₹10,000");

      // 9. Test POST /api/webhook (WhatsApp nurture simulation)
      const webhookRes = await request("POST", "/api/webhook", {
        action: "DISPATCH_WHATSAPP_DOSSIER",
        language: "te",
        leadData: {
          parentName: "వెంకటేష్",
          studentName: "సాయి తేజ",
          parentPhone: "+91 98480 23456",
        },
      });
      assert(webhookRes.statusCode === 200, "POST /api/webhook returns 200 OK");
      assert(webhookRes.body.dispatch.status === "SIMULATED_SUCCESS", "Webhook simulation dispatched successfully");
      assert(webhookRes.body.dispatch.dispatchedText.includes("నమస్కారం"), "WhatsApp template formatted in Telugu");

      // 10. Test GET / (HTML frontend serving)
      const htmlRes = await request("GET", "/");
      assert(htmlRes.statusCode === 200, "GET / serves static HTML 200 OK");
      assert(htmlRes.body.includes("NIAT ParentTrust AI"), "HTML contains NIAT ParentTrust AI title");

      console.log(`\n========================================`);
      console.log(`API TEST SUMMARY: ${passed} Passed, ${failed} Failed`);
      if (typeof server.closeAllConnections === "function") {
        server.closeAllConnections();
      }
      server.close((err) => {
        if (err) {
          console.error("Error closing server:", err);
          process.exit(1);
        }
        if (failed === 0) {
          console.log("✓ ALL LIVE API ENDPOINTS PASSED VERIFICATION!");
        } else {
          process.exit(1);
        }
      });
    } catch (err) {
      console.error("Test execution failed:", err);
      if (server) {
        if (typeof server.closeAllConnections === "function") server.closeAllConnections();
        server.close(() => process.exit(1));
      } else {
        process.exit(1);
      }
    }
  });
}

runApiTests();
