# alpaca-innovation


### Goal:

First the architecture design needs to be right.

Live Data Stream from ALPACA to Django DB to Sockets + External Postgres database, and from that directly to a source streaming Socket comm. server.

* Check lag - measure in seconds or milliseconds?

In an .`env` file, export `ALPACA_KEY_PAPER` and `ALPACA_SECRET_PAPER`.

`source .env`


# Basic FFT Transforms - `Applications of Fourier Transform to Smile Modeling`

Do NOT do this for options Black-Scholes-Merton for now, start on basic Fourier modelling over periods of time. FFT is not recommended for sensitive movements, use the full-fledged DFT transform.