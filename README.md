# Sample Merchant Application

Welcome to the NjiaPay Sample Merchant application!  
You can use this sample application as a spring board to get your application up and running with NjiaPay.

For full documentation on getting up and running on NjiaPay visit our [developer docs](https://docs.njiapay.com/)!

## Getting Started

### Prerequisites

- Python 3.14+
- An NjiaPay API key

### Installation

1. Clone the repository and move into it:

   ```sh
   git clone <repo-url>
   cd sample-merchant
   ```

2. Create a virtual environment and install dependencies. Any Python package manager works, e.g.:

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install .
   ```

   Or, if you use [uv](https://docs.astral.sh/uv/):

   ```sh
   uv sync
   ```

3. Configure environment variables. Create a `.env` file in the project root:

   ```sh
   API_KEY=your_njiapay_api_key
   API_URL=https://api-stg.njiapay.com   # optional, defaults to staging
   RETURN_URL=http://localhost:5000/payment-complete
   WEBHOOK_SECRETS=your_webhook_secret
   ```

   | Variable          | Required | Description                                                                                 |
   | ----------------- | -------- | ------------------------------------------------------------------------------------------- |
   | `API_KEY`         | Yes      | Your NjiaPay API key, sent as a bearer token                                                |
   | `API_URL`         | No       | NjiaPay API base URL (defaults to `https://api-stg.njiapay.com`)                            |
   | `RETURN_URL`      | No       | Where NjiaPay redirects after checkout (defaults to `https://example.com/payment-complete`) |
   | `WEBHOOK_SECRETS` | No       | Comma-separated signing secrets used to verify `/webhook` requests                          |

### Running the sample app

**Locally:**

```sh
flask --app sample_app.app run
```

(If using uv, prefix the command with `uv run`, e.g. `uv run flask --app sample_app.app run`.)

The app will be available at [http://localhost:5000](http://localhost:5000).

**With Docker Compose:**

```sh
docker compose up --build
```

This reads `API_KEY`, `API_URL`, and `WEBHOOK_SECRETS` from your shell environment (or a `.env` file) and exposes the app on port 5000.

### Trying it out

- Visit `/cart/regular` for a standard checkout flow, or `/cart/mit` to initiate a merchant-initiated-transaction (MIT) setup.
- After completing payment on NjiaPay's hosted page, you'll be redirected back to `/payment-complete`.
- Point your NjiaPay webhook configuration at `/webhook` to receive payment and refund lifecycle events.
