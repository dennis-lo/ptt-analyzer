# ptt-analyzer
A repository of scripts used to analyze articles posted on PTT


TODO:
- Add module that acts as a main function so that user can specify inputs through CLI more easily
- Add module that reads settings from configuration
- Add components to perform (rather simplified version of) text mining over the extracted content
  - Taggers, etc.
- Concurrency
  - Offload I/O tasks to individual workers
  - Alternative design with up to 2 task queues
- Add components to visualize the results
