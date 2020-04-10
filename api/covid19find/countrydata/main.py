from Countries import Country


def test_class(code, year, age):
    country = Country(code, year, age)
    print("\nExact data for %s in %s:" % (country.name, country.year))
    try:
        print("Total population: %.2f" % country.get_population())
    except TypeError:
        print("Total population: %s" % country.get_population())
    try:
        print("Hospital beds: %.2f" % country.get_hosp_beds())
    except TypeError:
        print("Hospital beds: %s" % country.get_hosp_beds())
    try:
        print("Percent urbanized: %.2f" % country.get_pcnt_urban())
    except TypeError:
        print("Percent urbanized: %s" % country.get_pcnt_urban())
    try:
        print("Percent degraded: %.2f" % country.get_pcnt_degraded())
    except TypeError:
        print("Percent degraded: %s" % country.get_pcnt_degraded())
    try:
        print("Number over %i: %.2f" % (age, country.get_overX()))
    except TypeError:
        print("Number over %i: %s" % (age, country.get_overX()))

    nearest = country.search_avail_stats()
    print("\nNearest available data for %s:" % country.name)
    try:
        print("population: %i, year: %s" % (nearest["pop"][1], nearest["pop"][0]))
    except TypeError:
        print("population: %s, year: %s" % (nearest["pop"][1], nearest["pop"][0]))
    try:
        print("percent urbanized: %.2f, year: %s" % (nearest["urban"][1], nearest["urban"][0]))
    except TypeError:
        print("percent urbanized: %s, year: %s" % (nearest["urban"][1], nearest["urban"][0]))
    try:
        print("degraded: %.2f, year: %s" % (nearest["degraded"][1], nearest["degraded"][0]))
    except TypeError:
        print("degraded: %s, year: %s" % (nearest["degraded"][1], nearest["degraded"][0]))
    try:
        print("over %i: %i, year: %s" % (country.age, nearest["overX"][1], nearest["overX"][0]))
    except TypeError:
        print("over %i: %s, year: %s" % (country.age, nearest["overX"][1], nearest["overX"][0]))
    try:
        print("hospital beds per 1000: %.2f, year: %s" % (nearest["hosp_beds"][1], nearest["hosp_beds"][0]))
    except TypeError:
        print("hospital beds per 1000: %s, year: %s" % (nearest["hosp_beds"][1], nearest["hosp_beds"][0]))
    try:
        print("high contact population: %.2f, year: %s" % (nearest["high_contact"][1], nearest["high_contact"][0]))
    except TypeError:
        print("high contact population: %s, year: %s" % (nearest["high_contact"][1], nearest["high_contact"][0]))
    try:
        print("remote population: %.2f, year: %s" % (nearest["remote"][1], nearest["remote"][0]))
    except TypeError:
        print("remote population: %s, year: %s" % (nearest["remote"][1], nearest["remote"][0]))


if __name__ == "__main__":
    code = 156
    year = 2010
    age = 65
    test_class(code, year, age)

    print('\n##################################\n')

    code = 4
    year = 2020
    age = 65
    test_class(code, year, age)
