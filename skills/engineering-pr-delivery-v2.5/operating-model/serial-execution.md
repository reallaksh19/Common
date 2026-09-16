# Serial execution and controlled parallelism

Default material execution mode is `SERIAL`. Read-only discovery may be broad, but no agent starts another material stream merely because it appears independent.

Parallelism requires an Owner-approved plan ID and ASCII topology shown before approval. The plan declares lanes/work packages, branch/worktree routing, write domains, shared reads, integration owner/EP, collision risks and stop conditions. Without explicit approval, material execution remains serial.