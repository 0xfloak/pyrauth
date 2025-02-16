A simple way to exchange TOTP codes with people.

Inspired by [PeerAuth](https://ksze.github.io/PeerAuth/)

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
