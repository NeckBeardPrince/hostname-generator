#!/bin/bash

# DC Comics
curl -X POST "http://localhost:8000/add_theme/dc" -H "Content-Type: application/json" -d '["batman", "robin", "superman", "wonder-woman", "joker", "flash", "green-lantern", "aquaman", "lex-luthor", "darkseid", "nightwing"]'

# Marvel
curl -X POST "http://localhost:8000/add_theme/marvel" -H "Content-Type: application/json" -d '["iron-man", "hulk", "thor", "black-widow", "spider-man", "doctor-strange", "black-panther", "loki", "venom", "deadpool"]'

# Dinosaurs 🦖
curl -X POST "http://localhost:8000/add_theme/dinosaurs" -H "Content-Type: application/json" -d '["t-rex", "velociraptor", "triceratops", "stegosaurus", "brachiosaurus", "ankylosaurus", "allosaurus", "diplodocus", "pteranodon", "spinosaurus"]'

# Mythology 🔥
curl -X POST "http://localhost:8000/add_theme/mythology" -H "Content-Type: application/json" -d '["zeus", "hera", "poseidon", "hades", "ares", "aphrodite", "odin", "thor", "loki", "freya", "anubis", "ra", "isis"]'

# Battle Star Galactica 🤖
curl -X POST "http://localhost:8000/add_theme/bsg" -H "Content-Type: application/json" -d '["galactica", "caprica", "pegasus", "cylon", "adama", "starbuck", "apollo", "boomer", "six", "baltar"]'

# Futurama 🚀
curl -X POST "http://localhost:8000/add_theme/futurama" -H "Content-Type: application/json" -d '["bender", "fry", "leela", "professor", "zoidberg", "hermes", "zapp-brannigan", "calculon", "robot-devil"]'

# Tech Giants 💻
curl -X POST "http://localhost:8000/add_theme/tech" -H "Content-Type: application/json" -d '["tesla", "spacex", "google", "apple", "microsoft", "ibm", "oracle", "nvidia", "amd", "intel"]'

# Cars 🏎️
curl -X POST "http://localhost:8000/add_theme/cars" -H "Content-Type: application/json" -d '["mustang", "corvette", "camaro", "porsche", "lamborghini", "ferrari", "mclaren", "tesla", "bugatti", "aston-martin"]'

# Star Wars ✨
curl -X POST "http://localhost:8000/add_theme/starwars" -H "Content-Type: application/json" -d '["yoda", "vader", "skywalker", "leia", "han-solo", "chewbacca", "palpatine", "grievous", "ahsoka", "kylo-ren"]'

# Star Trek
curl -X POST "http://localhost:8000/add_theme/startrek" -H "Content-Type: application/json" -d '["spock", "kirk", "riker", "picard", "janeway", "worf", "geordi", "data", "sulu", "uhura", "scotty", "crusher"]'

# Video Games 🎮
curl -X POST "http://localhost:8000/add_theme/gaming" -H "Content-Type: application/json" -d '["mario", "luigi", "link", "zelda", "samus", "kirby", "sonic", "megaman", "donkey-kong", "cloud", "sephiroth"]'
