
import express from "express";
import { paymentMiddleware } from "x402-express";
import fs from "fs";
import path from "path";

const app = express();
app.set("trust proxy", true);

// COLOQUE SEU ENDEREÇO PÚBLICO DA REDE BASE ABAIXO
const WALLET_ADDRESS = "0x2B2647D7326BC6f243b5b9c666Ff22611e4c9776";

app.use(
  paymentMiddleware(
    WALLET_ADDRESS,
    {
      "GET /api/gerador_de_dados": {
        price: "$0.10",
        network: "base",
        config: {
          description:
            "Structured JSON cybersecurity threat intelligence bulletin containing verified exploited vulnerabilities (CVEs), affected vendors, technical summaries, and remediation actions for AI agents and security pipelines.",
          mimeType: "application/json"
        }
      }
    }
  )
);

app.get("/api/gerador_de_dados", (req, res) => {
  try {
    const filePath = path.join(process.cwd(), "dataset.json");
    const rawContent = fs.readFileSync(filePath, "utf-8");
    const jsonData = JSON.parse(rawContent);

    res.setHeader("Content-Type", "application/json");
    return res.status(200).json(jsonData);
  } catch (error) {
    return res.status(500).json({
      error: "Failed to load cybersecurity dataset",
      details: error.message
    });
  }
});

export default app;

