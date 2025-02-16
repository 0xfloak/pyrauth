# PYRauth

A simple way to exchange TOTP codes with people.

Inspired by [PeerAuth](https://ksze.github.io/PeerAuth/)

## Motivation

Digital impersonation, in particular using deepfakes, is [on](https://www.dhs.gov/sites/default/files/publications/increasing_threats_of_deepfake_identities_0.pdf)
[the](https://www.jpmorgan.com/insights/fraud/fraud-protection/ai-scams-deep-fakes-impersonations-oh-my)
[rise](https://www.forbes.com/sites/bernardmarr/2024/11/06/the-dark-side-of-ai-how-deepfakes-and-disinformation-are-becoming-a-billion-dollar-business-risk/). While using shared context like memories can often suffice to verify identity, this method is vulnerable to replay attacks and leaks personal information to attackers.

Many people use authenticator apps for MFA in their day-to-day lives, so adding keys for contacts is as simple as scanning a QR code.

## Usage

1. Download and install requirements:

```
pip install -r requirements.txt
```

2. Run `python pyrauth.py <friend's name> <your name>`, where `<friend's name>` is the label that
will show next to the key in your authenticator app, and `<your name>` will show
in the other person's app.

3. Add the key using the printed QR code to your authenticator app.

4. Press any key to show the one for your friend.

  - *Optional* Press ENTER to generate codes and check them against the one in your app

5. Take a screenshot of the QR code *OR* use the `-o` or `--output-file` flag to save a PNG
you can share.

6. Send the image over a secure channel, preferably in person.

7. When you want to verify the person you're talking to is your friend/loved one/human relation,
open your authenticator app and read the code that shows under their name.

## Running without interactiveness

Use the `-q` or `--non-interactive` flags to just create QR codes.

## Testing codes from a premade URI

If you already generated a TOTP URI and just want to test code generation, you can import a URI
instead of generating a new one using the `--uri` option. This will still make fresh URIs for you
and your friend.
