"""ASLookup plugin for Errbot."""

from errbot import BotPlugin, botcmd

from aslookup.exceptions import LookupError
from aslookup.lookup import get_as_data


class ASLookup(BotPlugin):
    """IP-BGP data query plugin."""

    @botcmd(split_args_with=None)
    def aslookup(self, message, args):
        """
        Return AS routing data for input IP address(es).

        Look up IP address against BGP IP/AS lookup service. Only IPv4
        addresses are currently supported.

        """
        outs = []
        for ip in args:
            try:
                asdata = get_as_data(ip)
                outs.append(f"{ip:<15} {asdata.handle} {asdata.as_name}")
            except LookupError as e:
                yield f"{ip}: {e}"

        if outs:
            response = "\n".join(outs)
            self.send_card(body=f"```{response}```", in_reply_to=message)
        return
