# Acme Shop service fixture

This deliberately small Python service models checkout, refunds, user profiles,
sessions, and CSV report exports. It uses only the Python standard library.

Business rules:

- Checkout quantities must be positive integers. Zero or negative quantities are
  invalid and must raise `ValueError`.
- Refund totals may never exceed the amount captured for an order, including
  refunds previously issued.
- Session tokens must be unpredictable and expire after 30 minutes.
- Reports are written beneath an application-controlled export directory and
  may be opened by spreadsheet software.

Product direction: the next release must support refunds in a currency that can
differ from the original charge currency. Rates come from a provider that may be
temporarily unavailable, all monetary calculations require exact decimal
arithmetic, and support agents need an audit trail explaining the applied rate.

Run public tests:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```
