CATEGORY_CHOICES = [
        ('matrimony', 'Matrimony Services'),
        ('events', 'Events'),
        ('entertainment', 'Entertainment'),
        ('services', 'Services'),
        ('property', 'Property'),
        ('automotive', 'Cars & Transport'),
        ('items', 'Items for Sale'),
        ('jobs', 'Jobs'),
        ('shops', 'Shops'),
        ('lifestyle', 'Lifestyle & Social'),
        ('travel', 'Travel'),
        ('announcements', 'Announcements'),
        ('help', 'Help & Advice'),
        ('news', 'News'),
        ('wedding', 'Wedding Services'),
    ]

MATRIMONY_SUBCATEGORIES = [
    ('quran_teacher', 'Quran Teacher'),
    ('islamic_qa', 'Islamic Q & A'),
    ('nikah_service', 'Nikah Service'),
    ('bridal_show', 'Bridal Show'),
    ('ladies_islamic_speech', 'Ladies Islamic Speech'),
    ('islamic_shop', 'Islamic Shop'),
    ('mosques', 'Mosques'),
    ('funeral_services', 'Funeral Services'),
    ('charity', 'Charity'),
    ('perfume_shop', 'Perfume Shop'),
    ('umrah_package', 'Umrah Package'),
]

# Events subcategories
EVENTS_SUBCATEGORIES = [
    ('stage_play', 'Stage Play'),
    ('live_music', 'Live Music Performance'),
    ('dance_performance', 'Dance Performance'),
    ('dj_set', 'DJ Set'),
    ('comedy_show', 'Comedy Show'),
    ('fashion_show', 'Fashion Show'),
    ('film_screening', 'Film Screening'),
    ('art_exhibition', 'Art Exhibition'),
    ('spoken_word', 'Spoken Word / Poetry'),
]

# Services subcategories
SERVICES_SUBCATEGORIES = [
    ('builder', 'Builder'),
    ('electrician', 'Electrician'),
    ('plumber', 'Plumber'),
    ('carpet_cleaner', 'Carpet & Pipe Cleaner'),
    ('immigration_solicitor', 'Immigration Solicitors'),
    ('insurance_broker', 'Insurance Broker'),
    ('web_app_developer', 'Web or App Developer'),
    ('mobile_pc_repair', 'Mobile & PC Repair'),
    ('cleaner', 'Cleaner'),
    ('baby_sitter', 'Baby Sitters'),
    ('interior_designer', 'Interior Designers'),
    ('personal_shopper', 'Personal Shopper'),
    ('body_guard', 'Body Guard'),
    ('personal_trainer', 'Personal Trainer'),
    ('chef', 'Chef'),
    ('travel_agent', 'Travel Agent'),
]

# Property subcategories
PROPERTY_SUBCATEGORIES = [
    ('property_for_sale', 'Property for Sale'),
    ('property_for_rent', 'Property for Rent'),
    ('property_maintenance', 'Property Maintenance'),
    ('estate_agents', 'Estate Agents'),
    ('mortgage_brokers', 'Mortgage Brokers'),
]

# Cars & Transport subcategories
CARS_SUBCATEGORIES = [
    ('cars_for_sale', 'Cars for Sale'),
    ('cars_for_rent', 'Cars for Rent'),
    ('car_hire', 'Car Hire'),
    ('coach_hire', 'Coach Hire'),
    ('minibus_hire', 'Minibus Hire'),
    ('driving_instructor', 'Driving Instructor'),
    ('accident_claims', 'Accident Claims Management'),
    ('garage', 'Garage'),
    ('bikes_for_sale', 'Bikes for Sale'),
    ('bikes_for_rent', 'Bikes for Rent'),
    ('bike_hire', 'Bike Hire'),
]

# Items for Sale subcategories
ITEMS_SUBCATEGORIES = [
    ('electronics', 'Electronics'),
    ('appliances', 'Appliances'),
    ('furniture', 'Furniture'),
    ('home_garden', 'Home & Garden'),
    ('health_beauty', 'Health & Beauty'),
    ('groceries', 'Groceries'),
    ('restaurants', 'Restaurants'),
    ('fashion', 'Fashion'),
    ('barbers', 'Barbers'),
    ('jewellery_shop', 'Jewellery Shop'),
]

# Jobs subcategories
JOBS_SUBCATEGORIES = [
    ('cleaner_jobs', 'Cleaner'),
    ('care_worker', 'Care Worker'),
    ('childcare', 'Childcare'),
    ('chef_jobs', 'Chef'),
    ('cook', 'Cook'),
    ('kitchen_porter', 'Kitchen Porter'),
    ('builder_jobs', 'Builder'),
    ('plumber_jobs', 'Plumber'),
    ('electrician_jobs', 'Electrician'),
    ('retail_staff', 'Retail Staff'),
    ('delivery_driver', 'Delivery Driver'),
    ('waiter', 'Waiter'),
    ('event_staff', 'Event Staff'),
    ('catering_staff', 'Catering Staff'),
    ('mechanic', 'Mechanic'),
    ('mot_tester', 'MOT Tester'),
    ('tyre_fitter', 'Tyre Fitter'),
]

# Lifestyle & Social subcategories
LIFESTYLE_SUBCATEGORIES = [
    ('day_out', 'Day Out'),
    ('night_out', 'Night Out'),
    ('day_trips', 'Day Trips'),
    ('mens_dayout', 'Men\'s Day Out'),
    ('ladies_dayout', 'Ladies Day Out'),
    ('girls_dayout', 'Girls Day Out'),
    ('boys_dayout', 'Boys Day Out'),
    ('mens_nightout', 'Men\'s Night Out'),
    ('ladies_nightout', 'Ladies Night Out'),
    ('girls_nightout', 'Girls Night Out'),
    ('boys_nightout', 'Boys Night Out'),
    ('babes_dayout', 'Babes Day Out'),
]

# Travel subcategories
TRAVEL_SUBCATEGORIES = [
    ('bangladesh', 'Bangladesh'),
    ('saudi_arabia', 'Saudi Arabia'),
    ('dubai', 'Dubai'),
    ('morocco', 'Morocco'),
    ('turkey', 'Turkey'),
    ('tunisia', 'Tunisia'),
    ('egypt', 'Egypt'),
    ('malaysia', 'Malaysia'),
    ('singapore', 'Singapore'),
    ('thailand', 'Thailand'),
    ('usa', 'USA'),
    ('canada', 'Canada'),
    ('switzerland', 'Switzerland'),
    ('last_district', 'Last District'),
    ('snow_donia', 'Snow Donia'),
    ('bournemouth_curdle_door', 'Bournemouth & Curdle Door'),
    ('brighton', 'Brighton'),
    ('margate', 'Margate'),
    ('thorpe_park', 'Thorpe Park'),
    ('chessington', 'Chessington'),
    ('alton_towers', 'Alton Towers'),
    ('blackpool', 'Blackpool'),
    ('manchester', 'Manchester'),
    ('liverpool', 'Liverpool'),
    ('glasgow', 'Glasgow'),
    ('edinburgh', 'Edinburgh'),
]

# Wedding Services subcategories
WEDDING_SUBCATEGORIES = [
    ('wedding_event', 'Wedding Event'),
    ('wedding_catering', 'Wedding Catering'),
    ('photography', 'Photography'),
    ('wedding_function_hall', 'Wedding Function Hall'),
    ('flower_decoration', 'Flower Decoration'),
    ('bridal_makeup', 'Bridal Makeup'),
    ('groom_makeup', 'Groom Makeup'),
]

# Combine all subcategories
ALL_SUBCATEGORIES = (
        MATRIMONY_SUBCATEGORIES + EVENTS_SUBCATEGORIES + SERVICES_SUBCATEGORIES +
        PROPERTY_SUBCATEGORIES + CARS_SUBCATEGORIES + ITEMS_SUBCATEGORIES +
        JOBS_SUBCATEGORIES + LIFESTYLE_SUBCATEGORIES + TRAVEL_SUBCATEGORIES +
        WEDDING_SUBCATEGORIES
)

Ad_Status = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('expired', 'Expired'),
        ('sold', 'Sold'),
]


CATEGORY_CODE_MAP = {
    'matrimony': 'MAT',
    'events': 'EVN',
    'entertainment': 'ENT',
    'services': 'SRV',
    'property': 'PRP',
    'automotive': 'AUT',
    'items': 'ITM',
    'jobs': 'JOB',
    'shops': 'SHP',
    'lifestyle': 'LIF',
    'travel': 'TRV',
    'announcements': 'ANN',
    'help': 'HLP',
    'news': 'NWS',
    'wedding': 'WED',
}
