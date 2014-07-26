"""
1. user clicks "vizualize data"
pub id is sent to flask
query DB with a .get
create a dict where __?
root node is the main publication

2. get a list of pub's refs
3. get a list of pubs that ref
4. assign children (append every other)
"""

[
    {   "pubid": 137,
        "name": "Pub1, 1967",
        "parent": "null",
        "time": 1967,
        "relatedness": 10,
        "children": [
            {   "pubid": 127,
                "name": "Pub4, 1949",
                "parent": "Pub1, 1967",
                "time": 1949,
                "relatedness": 3,
                "children": [
                    {   "pubid": 46,
                        "name": "Pub8, 1936",
                        "parent": "Pub4, 1984",
                        "time": 1936,
                        "relatedness": 2
                    },
                    {   "pubid": 77,
                        "name": "Pub9, 1931",
                        "parent": "Pub4, 1984",
                        "time": 1931,
                        "relatedness": 9
                    }
                ]
            },
            {   "pubid": 12,
                "name": "Pub2, 1990",
                "parent": "Pub1, 1967",
                "time": 1990,
                "relatedness": 7,
                "children": [
                    {   "pubid": 17,
                        "name": "Pub6, 2000",
                        "parent": "Pub2, 1990",
                        "time": 2000,
                        "relatedness": 5
                    },
                    {   "pubid": 234,
                        "name": "Pub7, 2013",
                        "parent": "Pub2, 1990",
                        "time": 2013,
                        "relatedness": 1
                    }
                ]
            },
            {   "pubid": 127,
                "name": "Pub4, 1949",
                "parent": "Pub1, 1967",
                "time": 1949,
                "relatedness": 3,
                "children": [
                    {   "pubid": 46,
                        "name": "Pub8, 1936",
                        "parent": "Pub4, 1984",
                        "time": 1936,
                        "relatedness": 2
                    },
                    {   "pubid": 77,
                        "name": "Pub9, 1931",
                        "parent": "Pub4, 1984",
                        "time": 1931,
                        "relatedness": 9
                    }
                ]
            },
            {   "pubid": 67,
                "name": "Pub3, 1997",
                "parent": "Pub1, 1967",
                "time": 1997,
                "relatedness": 7
            },
            {   "pubid": 127,
                "name": "Pub4, 1949",
                "parent": "Pub1, 1967",
                "time": 1949,
                "relatedness": 3,
                "children": [
                    {   "pubid": 46,
                        "name": "Pub8, 1936",
                        "parent": "Pub4, 1984",
                        "time": 1936,
                        "relatedness": 2
                    },
                    {   "pubid": 77,
                        "name": "Pub9, 1931",
                        "parent": "Pub4, 1984",
                        "time": 1931,
                        "relatedness": 9
                    }
                ]
            },
            {   "pubid": 3,
                "name": "Pub5, 1981",
                "parent": "Pub1, 1967",
                "time": 1981,
                "relatedness": 3
            }
            
        ]
    }
];