<!--
Adapted from pstack's benchmark-checklist (cursor/plugins, skills/benchmark-checklist/SKILL.md).

MIT License

Copyright (c) 2026 Lauren Tan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-->

A claim whose value is a measured number (a time, a throughput, a speedup, a memory figure)
carries `measured` in the fourth column of its Claims row and this section in the same issue.
`verification claims list` fails while any answer is missing. Answer from a run, not from
reading the code; an answer may say how the issue's test establishes it.

### Measured: <claim-id>

| Question | Answer |
|---|---|
| limiter | What bounds the number: the resource or code path that stops it being twice as good, found by profiling a run that is not reported. If a change did not move the number, the limiter is why. |
| alternatives | What else the number could be measuring: the load generator, a cache, warmup, a busy machine, an error path that returns fast. |
| work-happened | Evidence that the work ran inside the timed region and its result was used: rows written, bytes read, responses counted, outputs checked as correct, not just present. |
| configured-alike | Whether every side ran as production runs it: same build, flags, versions, data, batching and cache state. A side on defaults compares configurations, not implementations. |
| within-limits | The arithmetic bound the result must respect: bandwidth, cores times cost per operation, and the share of the run the changed piece took (removing 10% of a run makes it at most about 11% faster). |
