def up(db):
    return [
        # db().users.update_many({}, {"$set": {"gender": "CAT5"}}),
        # db().users.find_one_and_update(
        #     {"_id": "a7459bdd-1830-46c3-b504-9754708aabe4"}, {"$set": {"email": "test@test.com"}}
        # ),
        # db().users.delete_one({"_id": "a7459bdd-1830-46c3-b504-9754708aabe4"}),
        db().users.insert_many(
            [
                {"_id": "266bf3ecf-5734-48c2-a7b0-f0895bc10fe3a"},
                {
                    "_id": "266bf3ecf-5734-48c2-a7b0-f0895bc10fea",
                    "_auth_user_id": "5975194d-0172-48d0-8324-0219455ff83a",
                    "color_preferences": {"compliance": "#FF4078", "wellness": "#53EEE8", "workload": "#D6F744"},
                    "created_at": "2020-08-20T00:45:09.718+0000",
                    "date_of_birth": None,
                    "diet": "NONE",
                    "email": "kriheli+787@work.co",
                    "first_name": None,
                    "gender": "MALE2",
                    "has_set_bed_wake_time": False,
                    "height_meters": None,
                    "integrations": {},
                    "last_name": None,
                    "last_seen": None,
                    "nominal_wake_time": "06:00",
                    "notification_types": [],
                    "push_notification_tokens": ["797C2A48EF0C93B2EC37EBF79B"],
                    "self_reports": [
                        {
                            "_id": "549ea96c-a589-4ac4-8ea7-abfb72f244c7",
                            "report_date": "2020-08-20T00:51:35.000+0000",
                            "motivation": 9.0,
                            "fatigue": 2.0,
                            "readiness": 8.5,
                        }
                    ],
                    "self_reports_push_notifications": [
                        {"scheduled_time": "2020-08-26T13:30:00.000+0000", "push_notification_url": "https://try.me",},
                        {"scheduled_time": "2020-08-21T13:30:00.000+0000", "push_notification_url": "https://try.me",},
                    ],
                    "supplements_recs_opt_in": False,
                    "sweat_profiles": [],
                    "sweat_profiles_count": 0,
                    "timezone": "America/Los_Angeles",
                    "unit_system": None,
                    "updated_at": "2020-08-20T00:51:35.995+0000",
                    "weight_kilograms": 68.0388555,
                    "timeline": [
                        {
                            "_id": "be678ecc-5a3c-490a-897e-3fc4b09a1430",
                            "pivot_id": None,
                            "copy": "",
                            "begin": "2020-08-19T14:49:00.000+0000",
                            "end": "2020-08-19T15:50:00.000+0000",
                            "type": "HIKE",
                            "duration_minutes": 61,
                            "kind": "WORKOUT",
                            "source": "USER",
                            "source_id": None,
                            "state": "EXECUTED",
                            "sRPE": 3.0,
                            "weigh_in_kilograms": None,
                            "weigh_out_kilograms": None,
                            "fluid_intake_milliliters": 0,
                            "sodium_loss_milligrams": None,
                            "location": None,
                            "temperature_celsius": None,
                            "distance_kilometers": None,
                            "training_load": 0.0,
                            "last_survey": "2020-08-20 00:49:20Z",
                            "sweat_profile_id": None,
                            "event_type": "HIKE",
                        }
                    ],
                    "migration_history": [
                        {
                            "date": "2020-08-20T00:50:48.201+0000",
                            "source": "66bf3ecf-5734-48c2-a7b0-f0895bc10fea",
                            "target": "5975194d-0172-48d0-8324-0219455ff83a",
                        }
                    ],
                },
            ]
        ),
    ]


def down(db):
    print("DOWN", db)
    return []
