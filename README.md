# trans

## Workflow concept

- Start listen server on game launch to handle request to start local translation server from squirrel

- Send request to said server to start translation server for match with `--load-only` and select supported languages from convar string e.g: `de,en,ru`

- Send request to translation server on newly received chat message with the message as query

- Duplicate message with appended translation 
  - > [ADV] Name: Выходные в Санкт-Петербурге
  - > [ADV] Name: Wochenende in St. Petersburg

- or translate message directly with indicator suffix  
  - > [ADV] Name: [ru-de] Wochenende in St. Petersburg