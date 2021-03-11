import os
import sys
import glob
import config
import pycountry
import pandas as pd


class Country:
    def set_name(self, data):
        country_key = data["country"]
        name_key = data["name"]
        df = data["data"]
        df = df.loc[df[country_key] == self.code]
        this_name = df[name_key].values
        self.name = this_name[0]

    def set_population(self, data):
        key = data["country"]
        units = data["units"]
        df = data["data"]
        try:
            df = df.loc[df[key] == self.code]
            pop = df[str(self.year)].values
            pop = int(pop[0])
            self.pop = pop * units
        except KeyError:
            #print("Population data not available for %s in %i" % (self.name, self.year))
            self.pop = None
            
    def set_income_category(self,data):
        key=data["country"]
        units = data["units"]
        df=data["data"]
        try:
            df = df.loc[df[key] == self.code]
            income_category = df[str(self.year)].values
  #  This is temporary fix because find_nearest function not working
    #        income_category = df[str(2019)].values
            income_category=income_category[0]
            self.income_category=income_category
        except KeyError:
            #print("Population data not available for %s in %i" % (self.name, self.year))
            self.income_category = None
        

    def set_active_pop(self, data):
        key = data["country"]
        units = data["units"]
        df = data["data"]
        try:
            df = df.loc[df[key] == self.code]
            active_pop = df[str(self.year)].values
            active_pop = int(active_pop[0])
            self.active_pop = active_pop * units * self.pop  # multiply by total pop since dataset is in % of total pop
        except KeyError:
            #print("Population data not available for %s in %i" % (self.name, self.year))
            self.active_pop = None

    def set_pcnt_urban(self, data):
        key = data["country"]
        units = data["units"]
        df = data["data"]
        try:
            df = df.loc[df[key] == self.code]
            urb = df[str(self.year)].values
            urb = int(urb[0])
            self.urban = urb * units
        except KeyError:
            #print("Percent urbanized data not available for %s in %i" % (self.name, self.year))
            self.urban = None

    def set_overX(self, data):
        country_key = data["country"]
        pop_key = data["total_pop"]
        year_key = data["year"]
        age_key = data["age"]
        units = data["units"]
        df = data["data"]
        try:
            df = df.loc[df[country_key] == self.code]
            df = df.loc[df[year_key] == self.year]
            assert not df.empty
            df = df[df[age_key] >= self.age]
            overX = df[pop_key].sum()
            self.overX = overX * units
        except (KeyError, AssertionError) as e:
            #print("Age-related data not available for %s in %i" % (self.name, self.year))
            self.overX = None

    def set_hosp_beds(self, data):
        key = data["country"]
        units = data["units"]
        df = data["data"]
        try:
            df = df.loc[df[key] == self.code]
            beds = df[str(self.year)].values
            beds = int(beds[0])
            self.hosp_beds = beds * units
        except KeyError:
            #print("Hospital bed data not available for %s in %i" % (self.name, self.year))
            self.hosp_beds = None

    def set_high_contact(self):
        #print("No data available for high contact populations.")
        self.high_contact = None

    def set_remote(self):
        #print("No data available for remote populations.")
        self.remote = None

    def set_pcnt_degraded(self):
        #print("No data available for degraded populations.")
        self.degraded = None

    def __init__(self, code, year, age=None):
        self.code = int(code)
        self.year = int(year)
        self.age = int(age)
        assert pycountry.countries.get(numeric=str(self.code).zfill(3)) is not None

        self.set_name(config.total_pop)
        self.set_population(config.total_pop)
        self.set_active_pop(config.active_pop)
        self.set_pcnt_urban(config.pcnt_urban)
        self.set_pcnt_degraded()
        self.set_overX(config.age_distr)
        self.set_hosp_beds(config.hospital_beds)
        self.set_high_contact()
        self.set_remote()
        self.set_income_category(config.income_category)

    def _find_nearest(self, data, year, attr):
        key = data["country"]
        units = data["units"]
        df = data["data"]
        df = df.loc[df[key] == self.code]
        if df.empty:
            return (getattr(self, attr), str(self.year))
        if attr == "overX":
            age_key = data["age"]
            year_key = data["year"]
            pop_key = data["total_pop"]
            idx = df.first_valid_index()
            closest_year = df.loc[idx]["Time"]
            df = df.loc[df[year_key] == closest_year]
            df = df[df[age_key] >= self.age]
            return (df[pop_key].sum() * units, str(closest_year))
        try:
            col = df.T[:str(year)]
        except KeyError:
            col = df.T
        closest_year = col.last_valid_index()
        if not closest_year:
            return (None, None)
        if attr=="income_category":
            val=col.loc[closest_year].values[0]
            return(val,str(closest_year))
        val = int(col.loc[closest_year].values[0])
        if attr == "active_pop":
            return (val * units * self.pop, str(closest_year))
        else:
            return (val * units, str(closest_year))

    def get_total_beds(self):
        if self.pop is None or self.hosp_beds is None:
            return None
        else:
            return (self.pop / 1000.0) * self.hosp_beds

    def search_avail_stats(self):
        subs = {}
        datasets = [config.total_pop, config.active_pop, config.pcnt_urban, None, config.age_distr, config.hospital_beds, None, None, config.income_category]
        attrs = ["pop", "active_pop", "urban", "degraded", "overX", "hosp_beds", "high_contact", "remote","income_category"]
        for data, attr in zip(datasets, attrs):
            subs[attr] = (getattr(self, attr), str(self.year))
            if getattr(self, attr) is None:
                if data is not None:
                    subs[attr] = self._find_nearest(data, self.year, attr)
        return subs

    def get_population(self):
        return self.pop

    def get_active_pop(self):
        return self.active_pop

    def get_pcnt_urban(self):
        return self.urban

    def get_overX(self):
        return self.overX

    def get_hosp_beds(self):
        return self.hosp_beds

    def get_high_contact(self):
        return self.high_contact

    def get_remote(self):
        return self.remote

    def get_pcnt_degraded(self):
        return self.degraded
    
    def get_income_category(self):
        return self.income_category
