# -*- coding: utf-8 -*-

import random
import string
from datetime import datetime, timedelta

from odoo import models, fields, api, tools

def random_name(self):
    letters = list(string.ascii_lowercase)
    first_strong = list(string.ascii_uppercase)
    vocals = ['a','e','i','o','u','']
    name = random.choice(first_strong)
    for i in range(0,random.randint(2,9)):
        name = name+random.choice(letters)+random.choice(vocals)
    return name



class king(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    #_name = 'emperor.king'
    _description = 'Kiing'

    is_king = fields.Boolean()
    #name = fields.Char(default=random_name)
    photo = fields.Image(max_width=100, max_heigth=150)
    level = fields.Integer()
    points = fields.Integer()
    age = fields.Integer()
    regiem = fields.Selection([('1','Democratic'),('2','Aristocratic'),('3','Oligarchic'),('4','Totalitarian'),('5','Dictatorial'),('6','Autotiraty')])
    sex = fields.Selection([('1','Man'),('2','Woman')])
    race = fields.Selection([('1','Elf'),('2','Human'),('3','Orc'),('4','Dark Elf'),('5','Giant'),('6','Fairy'),('7','Demon')])
    popularity = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('0','10')], computed='_set_popularity')
    ships = fields.One2many('emperor.ship', 'king')
    kingdoms = fields.One2many('emperor.kingdom', 'king')
    travels = fields.One2many('emperor.travel', 'king')
    levels = fields.One2many('emperor.levels', 'king')
    worlds = fields.Many2many('emperor.world')
    battles_a = fields.One2many('emperor.battle', 'attacker')
    battles_d = fields.One2many('emperor.battle', 'defender')
    kingdoms_owner = fields.One2many('emperor.kingdom', 'owner')
    kingdoms_owners = fields.One2many(related='kingdoms_owner')
    events = fields.Many2many('emperor.event')

    @api.model
    def _create_popularity(self):
        popularity ='1'


    @api.depends()
    def _set_popularity(self):
        for i in self:
            i.popularity = '1'


class ship(models.Model):
    _name = 'emperor.ship'
    _description = 'Ship'
    name = fields.Char()
    type_ship = fields.Selection([('1','Air'),('2','Land'),('3','Water'),('4','Underwater')])
    king = fields.Many2one('res.partner')
    kingdom = fields.Many2one('emperor.kingdom')


def kingdom_image(self):
    images = self.env['emperor.template'].search([]).mapped('photo')
    image = random.choice(images)

    return image


class kingdom(models.Model):
    _name = "emperor.kingdom"
    _description = "Kingdom"
    template = fields.Boolean()
    photo = fields.Image(default=kingdom_image, max_width=100, max_heigth=100)
    name = fields.Char(default=random_name)
    level = fields.Integer(default=random.randint(1, 100))
    residents = fields.One2many('emperor.people','inhabiting')
    plate = fields.Integer(default=random.randint(80, 130))
    gold = fields.Integer(default=random.randint(40, 90))
    diamonds = fields.Integer(default=random.randint(0, 50))
    image_small = fields.Binary(string='Image', compute='_get_images', store=True)
    king = fields.Many2one('res.partner')
    world = fields.Many2one('emperor.world', ondelete='cascade', required=True)
    ships = fields.One2many('emperor.ship', 'kingdom')

    attacker = fields.One2many('emperor.battle', 'attack')
    defender = fields.One2many('emperor.battle', 'defend')

    player_attacker = fields.One2many('emperor.battle', 'attacker')
    player_defender = fields.One2many('emperor.battle', 'defender')

    structures = fields.One2many('emperor.structure', 'built_in')
    attack_towers = fields.One2many('attack_tower.structure', 'built_in')
    defense_dome = fields.One2many('defense_dome.structure', 'built_in')
    nursery = fields.One2many('nursery.structure', 'built_in')
    power_stations = fields.One2many('power_station.structure', 'built_in')

    space_pos = fields.Integer(compute='_get_pos')

    owner = fields.Many2one('res.partner', ondelete="cascade")

    num_nur = fields.Integer(compute='_get_structures')
    production_xm = fields.Integer(compute='_get_structures')
    population = fields.Integer(compute='_get_structures')
    max_population = fields.Integer(compute='_get_structures')
    perc_population = fields.Integer(compute='_get_structures')

    num_ps = fields.Integer(compute='_get_structures')
    energy_xm = fields.Integer(compute='_get_structures')
    total_energy = fields.Integer(compute='_get_structures')
    max_energy = fields.Integer(compute='_get_structures')
    perc_energy = fields.Integer(compute='_get_structures')

    num_at = fields.Integer(compute='_get_structures')
    power_attack_xm = fields.Integer(compute='_get_structures')
    power_attack = fields.Integer(compute='_get_structures')
    max_power_attack = fields.Integer(compute='_get_structures')
    perc_power_attack = fields.Integer(compute='_get_structures')

    num_dd = fields.Integer(compute='_get_structures')
    power_defense_xm = fields.Integer(compute='_get_structures')
    power_defense = fields.Integer(compute='_get_structures')
    max_power_defense = fields.Integer(compute='_get_structures')
    perc_power_defense = fields.Integer(compute='_get_structures')


    def calculate_production(self):
        for k in self:
            if k.king:
                new_plate = k.plate * 0.001
                new_gold = k.gold * 0.001
                new_diamonds = k.diamonds * 0.001
                final_plate = k.plate + new_plate
                final_gold = k.gold + new_gold
                final_diamonds = k.diamonds + new_diamonds
                k.write({
                    'plate': final_plate,
                    'gold': final_gold,
                    'diamonds': final_diamonds
                })

    @api.model
    def update_resources(self):
        kingdoms = self.env['emperor.kingdom'].search([])
        kingdoms.calculate_production()
        print("Produccion actualizada")

    @api.depends()
    def _get_pos(self):
        for i in self:
            i.space_pos = i.id * 10 + random.randint(1, 9)

    @api.depends()
    def _get_structures(self):
        for w in self:
            w.num_structures = len(w.structures)
            for r in w.residents:
                w.population += 1

            # por tipo de estrucura
            for ps in w.power_stations:
                w.num_ps += 1
                # w.num_structures += 1
                w.energy_xm += ps.production_xm
                w.max_energy += ps.max_energy
                w.total_energy += ps.energy

            for n in w.nursery:
                w.num_nur += 1
                # w.num_structures += 1
                w.production_xm += n.production_xm
                w.max_population += n.capacity

            for at in w.attack_towers:
                w.num_at += 1
                # w.num_structures += 1
                w.power_attack_xm += at.production_xm
                w.power_attack += at.damage
                w.max_power_attack += at.max_damage

            for dd in w.defense_dome:
                w.num_dd += 1
                # w.num_structures += 1
                w.power_defense_xm += dd.production_xm
                w.max_power_defense += dd.max_buckler
                w.power_defense += dd.buckler

            if w.max_population > 0:
                w.perc_population = w.population * 100 / w.max_population
                if w.population > 0: w.perc_population -= 1
            if w.max_energy > 0:
                w.perc_energy = w.total_energy * 100 / w.max_energy
                if w.total_energy > 0: w.perc_energy -= 1
            if w.max_power_attack > 0:
                w.perc_power_attack = w.power_attack * 100 / w.max_power_attack
                if w.power_attack > 0: w.perc_power_attack -= 1
            if w.max_power_defense > 0:
                w.perc_power_defense = w.power_defense * 100 / w.max_power_defense
                if w.power_defense > 0: w.perc_power_defense -= 1


class world(models.Model):
    _name = "emperor.world"
    _description = "World"
    photo = fields.Image(max_width=100, max_heigth=100)
    name = fields.Char(default=random_name)
    riches = fields.Integer()
    kingdoms = fields.One2many('emperor.kingdom', 'world')
    kings = fields.Many2many('res.partner')

    def calculate_world(self):
        for o in self:
            if o.kings:
                new_riches = o.riches * 0.001
                final_riches = o.riches + new_riches
                o.write({
                    'riches': final_riches

                })

    @api.model
    def update_resources_world(self):
        world = self.env['emperor.world'].search([])
        world.calculate_world()
        print("World reactivate")



class travel(models.Model):
    _name = "emperor.travel"
    _description = "Travel"
    name = fields.Char(compute='_get_name')
    date = fields.Datetime()
    finish = fields.Date()
    hours = fields.Integer()
    king = fields.Many2one('res.partner')
    origin_kingdom = fields.Many2one('emperor.kingdom')
    destiny_kingdom = fields.Many2one('emperor.kingdom')
    launch_time = fields.Datetime(default=lambda t: fields.Datetime.now())

    @api.depends('origin_kingdom', 'destiny_kingdom', 'king')
    def _get_name(self):
        for t in self:
            t.name = str(t.king.name) + " " + str(t.origin_kingdom.name) + "-" + str(t.destiny_kingdom.name)

class levels(models.Model):
    _name = 'emperor.levels'
    king = fields.Many2one('res.partner')
    date = fields.Char(default=lambda self: fields.Datetime.now())
    levels = fields.Integer()

#Clase generar fichero de datos
class template(models.Model):
    _name = 'emperor.template'
    _description = 'of the emperor'
    name = fields.Char()
    photo = fields.Image()


class people(models.Model):
    _name = 'emperor.people'
    name = fields.Char()
    dead = fields.Boolean(default=False)
    live = fields.Integer(default=100)
    life_expectacy = fields.Integer(default=90)
    inteligence = fields.Integer()
    force = fields.Integer()
    ability = fields.Integer()

    def _get_date_now(self):
        date = datetime.now()
        return fields.Datetime.to_string(date)

    birth_date = fields.Datetime(default=_get_date_now)
    years = fields.Datetime(default=_get_date_now)

    inhabiting = fields.Many2one('emperor.kingdom')
    working = fields.Many2one('emperor.structure', ondelete='cascade', domain="[('built_in', '=', 'inhabiting')]")
    register = fields.One2many('emperor.history_people', 'registry')


class history_people(models.Model):
    _name = 'emperor.history_people'
    registry = fields.Many2one('emperor.people')




class structure(models.Model):
    _name = 'emperor.structure'
    name = fields.Char()
    template = fields.Boolean()

    cost = fields.Integer(default=20)
    completed = fields.Boolean(default=False)
    perc_complete = fields.Float('% Complete', (3, 2))
    lvl = fields.Integer()
    resource = fields.Integer()

    built_in = fields.Many2one('emperor.kingdom', ondelete='cascade')
    workers = fields.One2many('emperor.people', 'working')
    production_xm = fields.Float()
    energy_tax = fields.Integer()

    image = fields.Binary()
    image_lvl = fields.Binary()
    image_small = fields.Binary(string='Image', compute='_get_images', store=True)
    image_lvl_small = fields.Binary(string='Image', compute='_get_lvl_images', store=True)

    inc_int = fields.Integer()
    inc_frc = fields.Integer()
    inc_abt = fields.Integer()

    kanban_state = fields.Selection([
        ('start', 'Construction in progress'),
        ('blocked', 'Blocked'),
        ('producing', 'In production')],
        'Kanban State', default='start')

    @api.depends('image')
    def _get_images(self):
        for i in self:
            image = i.image
            i.image_small = image


    @api.depends('image_lvl')
    def _get_lvl_images(self):
        for i in self:
            image = i.image_lvl
            i.image_lvl_small = image

class power_station(models.Model):
    _name = 'power_station.structure'
    _inherits = {'emperor.structure': 'structure_id'}

    energy = fields.Integer(default=20)
    max_energy = fields.Integer(default=100)

    @api.model
    def up_lvl(self):
        if self.lvl == 3:
            ps_image = self.env.ref('emperor.power_station_lvl4')
            self.image_lvl = ps_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 15
            self.max_energy = 600
            self.energy_tax = 4
            self.inc_int = 2
            self.inc_frc = 3
            self.inc_abt = 6
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        if self.lvl == 2:
            ps_image = self.env.ref('emperor.power_station_lvl3')
            self.image_lvl = ps_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 10
            self.max_energy = 300
            self.energy_tax = 3
            self.inc_int = 3
            self.inc_frc = 4
            self.inc_abt = 7
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        if self.lvl == 1:
            ps_image = self.env.ref('emperor.power_station_lvl2')
            self.image_lvl = ps_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 7
            self.max_energy = 175
            self.energy_tax = 2
            self.inc_int = 4
            self.inc_frc = 5
            self.inc_abt = 8
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

class attack_tower(models.Model):
    _name = 'attack_tower.structure'
    _inherits = {'emperor.structure': 'structure_id'}

    damage = fields.Integer(default=40)
    max_damage = fields.Integer(default=400)

    @api.model
    def up_lvl(self):
        if self.lvl == 3:
            at_image = self.env.ref('emperor.attack_tower_lvl4')
            self.image_lvl = at_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 50
            self.max_damage = 1500
            self.energy_tax = 10
            self.inc_int = 2
            self.inc_frc = 3
            self.inc_abt = 3
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        if self.lvl == 2:
            at_image = self.env.ref('emperor.attack_tower_lvl3')
            self.image_lvl = at_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 16
            self.max_damage = 800
            self.energy_tax = 9
            self.inc_int = 3
            self.inc_frc = 4
            self.inc_abt = 4
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        if self.lvl == 1:
            at_image = self.env.ref('emperor.attack_tower_lvl2')
            self.image_lvl = at_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 8
            self.max_damage = 600
            self.energy_tax = 8
            self.inc_int = 4
            self.inc_frc = 5
            self.inc_abt = 5
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

class defense_dome(models.Model):
    _name = 'defense_dome.structure'
    _inherits = {'emperor.structure': 'structure_id'}

    buckler = fields.Integer(default=50)
    max_buckler = fields.Integer(default=200)

    @api.model
    def up_lvl(self):
        if self.lvl == 3:
            dd_image = self.env.ref('emperor.defense_dome_lvl4')
            self.image_lvl = dd_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 50
            self.max_buckler = 1500
            self.energy_tax = 8
            self.inc_int = 6
            self.inc_frc = 2
            self.inc_abt = 2
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        if self.lvl == 2:
            dd_image = self.env.ref('emperor.defense_dome_lvl3')
            self.image_lvl = dd_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 16
            self.max_buckler = 800
            self.energy_tax = 7
            self.inc_int = 7
            self.inc_frc = 3
            self.inc_abt = 3
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        if self.lvl == 1:
            dd_image = self.env.ref('emperor.defense_dome_lvl2')
            self.image_lvl = dd_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 8
            self.max_buckler = 600
            self.energy_tax = 6
            self.inc_int = 8
            self.inc_frc = 4
            self.inc_abt = 4
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

class nursery(models.Model):
    _name = 'nursery.structure'
    _inherits = {'emperor.structure': 'structure_id'}
    they_inhabit = fields.Integer(compute='_count_workers')
    capacity = fields.Integer(default=40)

    @api.model
    def _count_workers(self):
        for n in self:
            n.they_inhabit = len(n.workers)

    @api.model
    def up_lvl(self):
        if self.lvl == 3:
            n_image = self.env.ref('emperor.nursery_lvl4')
            self.image_lvl = n_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 32
            self.capacity = 320
            self.energy_tax = 7
            self.inc_int = 7
            self.inc_frc = 3
            self.inc_abt = 2
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        if self.lvl == 2:
            n_image = self.env.ref('emperor.nursery_lvl3')
            self.image_lvl = n_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 16
            self.capacity = 160
            self.energy_tax = 6
            self.inc_int = 7
            self.inc_frc = 4
            self.inc_abt = 3
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        if self.lvl == 1:
            n_image = self.env.ref('emperor.nursery_lvl2')
            self.image_lvl = n_image.image_lvl
            self.lvl = self.lvl + 1
            self.production_xm = 8
            self.capacity = 80
            self.energy_tax = 5
            self.inc_int = 8
            self.inc_frc = 5
            self.inc_abt = 4
            self.completed = False
            self.perc_complete = 0
            self.kanban_state = 'start'
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }


class battle(models.Model):
    _name = 'emperor.battle'
    name = fields.Char(default='Battle')
    finished = fields.Boolean(default='False')

    attacker = fields.Many2one('res.partner')
    defender = fields.Many2one('res.partner')

    attack = fields.Many2one('emperor.kingdom')
    defend = fields.Many2one('emperor.kingdom')

    image_attack = fields.Binary(compute='_getImages')
    image_defend = fields.Binary(compute='_getImages')

    distance = fields.Integer()
    damage = fields.Integer()

    start_date = fields.Datetime()
    end_date = fields.Datetime()

    @api.model
    def _getImages(self):
        for a in self.attack:
            self.image_attack = a.image_small
        for d in self.defend:
            self.image_defend = d.image_small



    def compute_battle(self):
        date_now = datetime.now()
        for b in self:
            if b.end_date <= date_now:
                dm_for_dd = b.damage / b.defend.num_dd
                for dd in b.defend.defense_dome:
                    dd.buckler = dd.buckler-dm_for_dd
                b.finished = True

class event(models.Model):
    _name = 'emperor.event'
    name = fields.Char()
    player_inc = fields.Many2many('res.partner')

    date = fields.Datetime()
    end_date = fields.Datetime()

    tipe_event = fields.Selection([
        ('attack', 'Battle'),
        ('exchange', 'Treatment'),
        ('union_petition', 'Request')])
