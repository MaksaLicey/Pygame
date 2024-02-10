import sys


def get_coordinates(toponym):
    return 1, 1


def show_map(var1, var2, var=''):
    pass


def get_ll_span(var1):
    return 1, 1


def main():
    api_key = "d8f4fbf5-ca85-4e77-a9ff-61a96364f374"

    address_ll = "37.588392,55.734036"
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    toponym_to_find = " ".join(sys.argv[1:])

    if toponym_to_find:
        lat, lon = get_coordinates(toponym_to_find)
        ll_spn = f"ll={lat},{lon}&spn=0.005,0.005"
        show_map(ll_spn, "map")

        ll, spn = get_ll_span(toponym_to_find)
        ll_spn = f'll={ll}&spn={spn}'
        # show_map(ll_spn, "map", add_params=point_param)

    else:
        print("ага!")


if __name__ == '__main__':
    main()
