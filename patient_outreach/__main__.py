"""Command-line pilot sizing tool."""
import argparse
import json

from .power import Pilot


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=float, default=0.315)
    parser.add_argument("--effect", type=float, default=0.026)
    parser.add_argument("--capacity", type=float, default=0.2)
    parser.add_argument("--concentration", type=float, default=2.0)
    parser.add_argument("--capture", type=float, default=0.7)
    parser.add_argument("--allocation", type=float, default=0.5)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--attrition", type=float, default=0.05)
    parser.add_argument("--cluster-size", type=float, default=1)
    parser.add_argument("--icc", type=float, default=0)
    parser.add_argument("--enrollment", type=int, default=60000)
    parser.add_argument("--power", type=float, default=0.8)
    options = vars(parser.parse_args())
    n, target = options.pop("enrollment"), options.pop("power")
    try:
        pilot = Pilot(**options)
        uniform, targeted = pilot.rates()
        print(json.dumps({"kind": "scenario", "uniform_rate": uniform, "targeted_rate": targeted,
                          "power_at_enrollment": pilot.power(n), "required_enrollment": pilot.enrollment(target)}))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
