new_user = ("Hello {}!, Welcome to BlockNexus🤖\n\n"
            "I am a crypto currency exchange bot. I can convert\n"
            "any currency, i.e <b>BTC</b>, to any other currency, i.e <b>ETH</b>\n\n"
            "Check 'help' to get a full guide of bot usage.")

exist_user = ("Hello Again {}\n\n"
              "<b>To started</b>, tap the left <b>Menu ≡</b> button to\n"
              "access currency exchange💱.\n\n"
              "Check 'help' to see the list of supported currencies")

currency_from_msg = ("<b>BlockNexus:</b>\n\n"
                   "<code>Currency From: {}</code>\n"
                   "<code>Amount: {} (${})</code>\n\n"
                   "<em>Now select the currency to convert to:</em>")

currency_to_msg = ("<b>BlockNexus:</b>\n\n"
                  "<code>Currency From: {}</code>\n"
                  "<code>Currency to: {}</code>\n"
                  "<code>Amount: {} (${})</code>\n\n")

currency_review = ("<b>BlockNexus:</b>\n\n"
                   "<code>Currency From: {}</code>\n"
                   "<code>Currency to: {}</code>\n"
                   "<code>Amount: {} (${})</code>\n"
                   "<code>Receiving address: {}</code>\n\n"
                   "<em>Confirm Info or Return</em>")

exchange_confirm_msg = ("<b>BlockNexus (Exchange order Created):</b>\n\n"
                        "<code>Currency From: {}</code>\n"
                        "<code>Currency to: {}</code>\n"
                        "<code>Amount: {} (${})</code>\n"
                        "<code>Receiving address: {}</code>\n\n"
                        "<b>Send {} to this address:</b>\n"
                        "{}\n"
                        "<b>Send Exactly:</b> {}\n"
                        "------------------------------[+]\n"
                        "<code>Time: {}</code>\n"
                        "------------------------------[+]")

currency_rates_msg = ("<b>CRYPTO CURRENCY RATES📈</b>:\n"
                "Here is a list of the current supported <b>Crypto</b> to <b>USD</b> rates:\n"
                "{}\n"
                "<em>Bot's supported crypto currencies💱</em>")

exchange_history_msg = ("--------------------------------[+]\n"
                        "Order ID : <b>#{}</b>           [+]\n"
                        "--------------------------------[+]\n"
                        "<code>Currency from: {}\n"
                        "Curreny to: {}\n"
                        "Receive Address: {}\n"
                        "Amout: {} (${})</code>\n"
                        "--------------------------------[+]")