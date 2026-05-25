from .models import RawRecord, NormalizedRecord

def normalize_record(raw_record):

    data = raw_record.raw_data

    source = raw_record.source.source_type

    normalized = {
        "scope": "",
        "activity_type": "",
        "quantity": 0,
        "unit": ""
    }

    if source == "SAP":
        normalized["scope"] = "Scope 1"
        normalized["activity_type"] = "Fuel"
        normalized["quantity"] = data.get("quantity", 0)
        normalized["unit"] = "Liters"

    elif source == "UTILITY":
        normalized["scope"] = "Scope 2"
        normalized["activity_type"] = "Electricity"
        normalized["quantity"] = data.get("quantity", 0)
        normalized["unit"] = "kWh"

    elif source == "TRAVEL":
        normalized["scope"] = "Scope 3"
        normalized["activity_type"] = "Business Travel"
        normalized["quantity"] = data.get("distance", 0)
        normalized["unit"] = "km"

    return NormalizedRecord.objects.create(
        raw_record=raw_record,
        scope=normalized["scope"],
        activity_type=normalized["activity_type"],
        quantity=normalized["quantity"],
        unit=normalized["unit"]
    )