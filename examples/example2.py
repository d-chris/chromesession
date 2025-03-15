from chromesession import soups


def main():
    urls = [
        "https://example.com/",
        "https://example.com/",
    ]

    for bs in soups(
        urls,
        cache_name="caching.sqlite",
        verbose=False,
    ):
        print(bs.title)


if __name__ == "__main__":
    main()
