from Countries import Country


def print_message(message, value):
    for k, (m, v) in enumerate(zip(message, value)):
        if k == len(message)-1: end = '\n'
        else: end = ', '
        try:
            print((m + " %.2f") % v, end = end)
        except TypeError:
            print((m + " %s") % v, end = end)


def test_class(code, year, age):
    country = Country(code, year, age)

    print("\nExact data for %s in %s:" % (country.name, country.year))
    print_message(["Total population:"], [country.get_population()])
    print_message(["Hospital beds per 1000:"], [country.get_hosp_beds()])
    print_message(["Total hospital beds:"], [country.get_total_beds()])
    print_message(["Percent urbanized:"], [country.get_pcnt_urban()])
    print_message(["Percent degraded:"], [country.get_pcnt_degraded()])
    print_message(["Population over %i:" % int(age)], [country.get_overX()])

    nearest = country.search_avail_stats()
    print("\nNearest available data for %s:" % country.name)
    print_message(["Total population:", "year:"], [nearest["pop"][0], nearest["pop"][1]])
    print_message(["Hospital beds per 1000:", "year:"], [nearest["hosp_beds"][0], nearest["hosp_beds"][1]])
    print_message(["Total hospital beds:"], [(nearest["pop"][0] / 1000.0)*nearest["hosp_beds"][0]])
    print_message(["Percent urbanized:", "year:"], [nearest["urban"][0], nearest["urban"][1]])
    print_message(["Percent degraded:", "year:"], [nearest["degraded"][0], nearest["degraded"][1]])
    print_message(["Population over %i:" % int(age), "year:"], [nearest["overX"][0], nearest["overX"][1]])
    print_message(["High contact:", "year:"], [nearest["high_contact"][0], nearest["high_contact"][1]])
    print_message(["Remote:", "year:"], [nearest["remote"][0], nearest["remote"][1]])


if __name__ == "__main__":
    code = '756' #That's switzerland
    year = '2020'
    age = '65'
    test_class(code, year, age)

    print('\n##################################\n')

    code = '4'
    year = '2020'
    age = '65'
    test_class(code, year, age)

    print('\n##################################\n')

    code = '276'
    year = '2020'
    age = '65'
    test_class(code, year, age)

    print('\n##################################\n')

    code = '032'
    year = '2020'
    age = '65'
    test_class(code, year, age)

    print('\n##################################\n')
