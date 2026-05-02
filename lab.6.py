async function* generateUserEvents(total) {
  let id = 1;

  while (id <= total) {
    if (Math.random() < 0.00001) {
      throw new Error(`Generator error at event ${id}`);
    }

    yield {
      userId: id,
      action: Math.random() > 0.5 ? "click" : "view",
      amount: Math.random() * 500,
      createdAt: Date.now(),
    };

    id++;
  }
}

async function main() {
  const stream = generateUserEvents(1_000_000);

  let processed = 0;
  let totalClickAmount = 0;

  try {
    for await (const event of stream) {
      if (event.action === "click") {
        totalClickAmount += event.amount;
      }

      processed++;

      if (processed % 10000 === 0) {
        console.log(`Processed ${processed} events`);
      }
    }
  } catch (err) {
    console.error("Stream error:", err.message);
    throw err;
  }

  console.log("Finished processing");
  console.log("Total click amount:", totalClickAmount.toFixed(2));
}

main().catch(err => console.error("Fatal:", err.message));