# Design review

Team: Nguyen Tung Lam - V202603373
AI tool/model, or "manual": Antigravity (Gemini 3.8 Flash)

Write at most 200 words total. Refer to requirements, code or test assertions.

1. **Architecture:** Defend one application deployable and one database for
   this team. Give one cost and one potential benefit of a microservice split.

   Answer: A modular monolith suits this small team by guaranteeing local ACID transactional consistency and minimizing operational overhead. A microservice split introduces distributed transaction complexity across boundaries (cost), but allows isolated horizontal scaling of notification workloads (benefit).

2. **Patterns:** What does Strategy vary? What does Decorator add? Why is
   Observer optional while notification is the only reaction?

   Answer: Strategy varies notification delivery mechanisms (email, SMS, push) interchangeably via `NotificationChannel` (OCP). Decorator dynamically adds audit event recording without altering the underlying channel contract. Observer is unnecessary because notification is the sole synchronous reaction to task assignment.

3. **Changed requirement R6:** What must be written atomically? Who relays it?
   Why can duplicates occur? State one condition needed for eventual acceptance.

   Answer: The assigned task and outbox notification record must be written atomically in one database transaction. An asynchronous outbox worker relays it. Duplicates occur if the relay crashes after provider acceptance but before marking the outbox record sent. Downstream idempotency is required for safe eventual acceptance.

4. **Independent evidence:** Name one assertion you inspected and its matching
   sequence message or branch. What remains unverified by the offline tests?

   Answer: In `test_save_happens_before_send`, `self.assertEqual(trace, ['get', 'save', 'send'])` verifies `save` commits before `send` in the success sequence. Offline tests cannot verify real database crash recovery, persistent ACID durability, or network timeouts.
