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