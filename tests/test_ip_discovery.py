from aiohomekit.controller.ip import IpDiscovery, IpPairing


async def test_pair(controller_and_unpaired_accessory):
    discovery = IpDiscovery(
        controller_and_unpaired_accessory,
        {
            "name": "TestDevice._hap._tcp.local.",
            "address": "127.0.0.1",
            "port": 51842,
            "id": "00:01:02:03:04:05",
            "ff": 1,
        },
    )

    pairing = await discovery.perform_pairing("alias", "031-45-154")

    assert isinstance(pairing, IpPairing)

    assert await pairing.get_characteristics([(1, 9)]) == {
        (1, 9): {"value": False},
    }


async def test_identify(controller_and_unpaired_accessory):
    discovery = IpDiscovery(
        controller_and_unpaired_accessory,
        {
            "name": "TestDevice._hap._tcp.local.",
            "address": "127.0.0.1",
            "port": 51842,
            "id": "00:01:02:03:04:05",
        },
    )

    identified = await discovery.identify()
    assert identified is True
