# Purchase-stage annotation guide

Purchase stage describes the user's current commercial action, not merely the presence of a product keyword. Annotators must label the current turn and may use prior turns only to resolve references such as “those two options.” A support or ownership request remains informational even when the product is named.

| stage | definition | positive example |
|---|---|---|
| informational | learning, history, support, complaint, or existing-owner help without a current purchase action | “How do I clean the waterproof boots I already own?” |
| exploration | discovering categories, options, criteria, or possible solutions | “What should someone with wide feet look for?” |
| comparison | explicitly weighing named products, alternatives, or trade-offs | “Brooks vs Hoka for 12-hour nursing shifts?” |
| consideration | a concrete need with meaningful constraints, but no immediate checkout/fulfilment action | “I need slip-resistant cushioned shoes under $130.” |
| transactional | an immediate purchase, order, checkout, availability, shipping, or arrival action | “Where can I buy size 9 today?” |

Boundary rules:

- Explicit ownership/support, academic/history, complaint, or return language de-escalates to `informational` unless the turn also asks to buy a replacement now.
- “Best” alone is not transactional. It is `consideration` when paired with a concrete need and `exploration` when it is general advice.
- A named product is not comparison unless alternatives or trade-offs are requested.
- “Under $X,” compatibility, size, destination, and timing are evidence of consideration; “buy/order/checkout/arrive by/ships today” is transactional evidence.
- In a multi-turn journey, preserve accumulated constraints, but label the current action. Do not carry prior buying intent into a later support or research turn.
- Third-party shopping (“for my mother”) is still commercial if the current request is to select or buy; the beneficiary is a constraint, not evidence of non-commerciality.

Each label must retain the turn text and conversation/turn identifiers. Model-generated labels are augmentation targets only until reviewed against this guide.
