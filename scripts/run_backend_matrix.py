from __future__ import annotations


def main() -> None:
    backends = ["tdx", "sev", "trustzone", "keystone"]
    for name in backends:
        print(f"TODO: run protected workload with backend={name}")


if __name__ == "__main__":
    main()
