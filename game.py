# Description: Game class
import random

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from door import Door
from quest import Quest 

class Game:
    """The Game class manages the overall game state and flow."""

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.characters = []
        self.player = None
        self.items = {}

    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (Up, E, Down, O)", Actions.go, 1)
        self.commands["go"] = go
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        back = Command("back", " : revenir dans la salle précédente", Actions.back, 0, consumes_turn=False)
        self.commands["back"] = back
        look = Command("look", " : regarder les items présents dans la salle", Actions.look, 0, consumes_turn=False)
        self.commands["look"] = look
        take = Command("take", " <item> : prendre un objet", Actions.take, 1, consumes_turn=True)
        self.commands["take"] = take
        drop = Command("drop", " <item> : déposer un objet", Actions.drop, 1, consumes_turn=True)
        self.commands["drop"] = drop
        check = Command("check", " : vérifier l'inventaire du joueur", Actions.check, 0, consumes_turn=False)
        self.commands["check"] = check
        talk = Command("talk"," : parler à un PNJ", Actions.talk, 1, consumes_turn=False)
        self.commands["talk"] = talk
        fight = Command("fight"," : combattre un ennemi", Actions.fight, 1, consumes_turn=True)
        self.commands["fight"] = fight
        self.commands["quests"] = Command("quests"
                                          , " : afficher la liste des quêtes"
                                          , Actions.quests
                                          , 0)
        self.commands["quest"] = Command("quest"
                                         , " <titre> : afficher les détails d'une quête"
                                         , Actions.quest
                                         , 1)
        self.commands["activate"] = Command("activate"
                                            , " <titre> : activer une quête"
                                            , Actions.activate
                                            , 1)
        self.commands["rewards"] = Command("rewards"
                                           , " : afficher vos récompenses"
                                           , Actions.rewards
                                           , 0)
        sell = Command("sell", " : vendre un objet", Actions.sell, 0, consumes_turn=False)
        self.commands["sell"] = sell
        buy = Command("buy", " : acheter un objet", Actions.buy, 0, consumes_turn=False)
        self.commands["buy"] = buy
        train = Command("train", " : s'entraîner auprès d'un maître", Actions.train, 0, consumes_turn=False)
        self.commands["train"] = train
        upgrade = Command("upgrade", " : améliorer une arme auprès d'un forgeron", Actions.upgrade, 0, consumes_turn=False)
        self.commands["upgrade"] = upgrade


        # Setup rooms

        howling_cliffs = Room("Howling Cliffs", "non loin des frontières du royaume située au nord-ouest. Les falaises hurlantes n'ont pas l'air peuplées du tout.")
        self.rooms.append(howling_cliffs)
        self.dirtmouth = Room("Dirtmouth", "dans un petit village presque abandonné, nommé Dirtmouth. Il y a quand même un peu de lumière et de vie cependant. (Une des maisons semble être une sorte de magasin mais il est actuellement fermé)")
        self.rooms.append(self.dirtmouth)
        crystal_peak = Room("Crystal Peak", "à une certaine hauteur, dans un lieu scintillant prénommé Mont Cristal. De nombreuses mines ont été creusées dans la falaise pour obtenir les précieux cristaux roses.")
        self.rooms.append(crystal_peak)
        greenpath = Room("Greenpath", "à Vertchemin, un lieu dont la végétation luxuriante et les insectes recouverts de feuillage en font un endroit splendide. On trouve également des flaques d'acides brûlant et une épaisse prolifération rendant la navigation difficile.")
        self.rooms.append(greenpath)
        self.forgotten_crossroads = Room("Forgotten Crossroads", "au beau milieu des Routes Oubliées, situé sous le village de Dirtmouth. Elles permettaient autrefois de rejoindre de nombreuses autres régions du royaume.")
        self.rooms.append(self.forgotten_crossroads)
        temple_black_egg = Room("Temple of the Black Egg", "en face du Temple de l'Œuf Noir, on peut y entendre que quelque chose crie depuis l'intérieur et qu'un évènement risque de déterminer l'avenir du royaume.")
        self.rooms.append(temple_black_egg)
        blue_lake = Room("Blue Lake", "en face d'un lac bleu. Celui ci semble inoffensif et reposant à un tel point que l'on souhaiterait rester en face jusqu'à l'écroulement d'Hallownest.")
        self.rooms.append(blue_lake)
        fog_canyon = Room("Fog Canyon", "dans Brumes Canyon, un endroit effervescent et gélatineux de part les méduses qui y habitent. Cependant, gare à vous car les méduses peuvent exploser au contact d'une paroi tout comme leur nid. Une énorme structure s'y trouve.")
        self.rooms.append(fog_canyon)
        fungal_wastes = Room("Fungal Wastes", "dans la Caverne Nocive qui est une zone humide et recouverte de champignons de toutes les sortes. En plus de cela, des flaques d'acide caustiques sont abondantes dans toute la région.")
        self.rooms.append(fungal_wastes)
        city_of_tears = Room("City Of Tears", "dans la Cité des Larmes. C'était la capitale d'Hallownest. Elle est couverte d'une pluie perpétuelle qui provient du plafond qui la surplombe étant donné qu'elle est située en dessous du Lac Bleu. Son nom original a été perdu dans l'histoire. En plein centre de la Cité se trouve la place de la Fontaine, où se trouve la fontaine commémorative du Hollow Knight.")
        self.rooms.append(city_of_tears)
        mantis_village = Room("Mantis Village","dans le Village des Mantes. Un endroit où l'honneur et la souveraineté ne sont pas ceux du royaume d'Hallownest. Un pacte a été effectué pour qu'elle conserve la souveraineté sur leur domaine en échange de garder à distance les horribles bêtes du Nid Profond. Un village de guerriers et de guerrières qui défendent leur territoire au péril de leur vie !")
        self.rooms.append(mantis_village)
        deepnest = Room("Deepnest", "dans le Nid Profond. Son environnement lugubre et sombre, jonché d'épaisses couches de toile d'araignées, peut en faire fuir beaucoup. Malgré tout, des traces d'anciennes civilisations sont présentes, ce qui en fait un lieu riche en histoire.",dark=True)
        self.rooms.append(deepnest)

        # Create exits for rooms

        howling_cliffs.exits = {"Up" : None, "E" : self.dirtmouth, "Down" : greenpath, "O" : None}
        self.dirtmouth.exits = {"Up" : None, "E" : crystal_peak, "Down" : self.forgotten_crossroads, "O" : howling_cliffs}
        crystal_peak.exits = {"Up" : None, "E" : None, "Down" : None, "O" : self.dirtmouth}
        greenpath.exits = {"Up" : howling_cliffs, "E" : self.forgotten_crossroads, "Down" : fog_canyon, "O" : None}
        self.forgotten_crossroads.exits = {"Up" : self.dirtmouth, "E" : Door(temple_black_egg,locked=True), "Down" : fungal_wastes, "O" : greenpath}
        temple_black_egg.exits = {"Up" : None, "E" : blue_lake, "Down" : None, "O" : self.forgotten_crossroads}
        blue_lake.exits = {"Up" : crystal_peak, "E" : None, "Down" : None, "O" : temple_black_egg}
        fog_canyon.exits = {"Up" : greenpath, "E" : fungal_wastes, "Down" : None, "O" : None}
        fungal_wastes.exits = {"Up" : self.forgotten_crossroads, "E" : Door(city_of_tears, locked=True, key= "blason de la ville"), "Down" : mantis_village, "O" : fog_canyon}
        city_of_tears.exits = {"Up" : None, "E" : None, "Down" : None, "O" : fungal_wastes}
        mantis_village.exits = {"Up" : fungal_wastes, "E" : None, "Down" : deepnest, "O" : None}
        deepnest.exits = {"Up" : mantis_village, "E" : None, "Down" : None, "O" : None}

        #create items for rooms
        journal_vagabond_1 = Item("journal vagabond 1", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", value=500)
        journal_vagabond_2 = Item("journal vagabond 2", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", value=500)
        journal_vagabond_3 = Item("journal vagabond 3", "Ces journaux nous offrent un aperçu intéressant des esprits et des cœurs de ceux qui ont vécu avant nous.", value=500)
        lanterne = Item("lanterne", "Une lanterne en cristal qui éclaire les cavernes plongées de Deepnest afin que les voyageurs puissent retrouver leur chemin.", value=2000)
        self.items[lanterne.name] = lanterne
        minerai_pale_1 = Item("minerai pale 1", "Un minerai rare et pale, prié par ceux qui fabriquent des armes.", value=0)
        minerai_pale_2 = Item("minerai pale 2", "Un minerai rare et pale, prié par ceux qui fabriquent des armes.", value=0)
        cle_marchand = Item("cle du marchand", "Une clé de cuivre qui ouvre la boutique du Marchand à Dirtmouth.", value=1)
        sceau_hallownest_1 = Item("sceau hallownest 1", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", value=1000)
        sceau_hallownest_2 = Item("sceau hallownest 2", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", value=1000)
        sceau_hallownest_3 = Item("sceau hallownest 3", "Ces sceaux ornés étaient les symboles officiels du Roi et de ses Chevaliers, et étaient précieux de ceux qui les portaient.", value=1000)
        trampass = Item("trampass", "Un laissez-passer ancien qui permet d'utiliser les tramways du royaume.", value=0)
        idole_roi_1 = Item("idole du roi 1", "Une icône du roi de Hallownest, vénéré à la fois comme dieu et comme souverain. Fabriqués dans un matériau blanc mystérieux, ils sont rares et très précieux.", value=1500)
        idole_roi_2 = Item("idole du roi 2", "Une icône du roi de Hallownest, vénéré à la fois comme dieu et comme souverain. Fabriqués dans un matériau blanc mystérieux, ils sont rares et très précieux.", value=1500)
        blason_ville = Item("blason de la ville", "dalle de pierre arborant le blason de la capitale d'Hallownest.", value=1000)
        self.items[blason_ville.name] = blason_ville
        masque_erudite = Item("masque de l'érudite", "Un masque ancien qui augmente votre sagesse.", value=0)
        aiguillon = Item("aiguillon", "Un aiguillon simple mais efficace pour combattre les ennemis.", value=0)
        oeuf_arcanique = Item("oeuf arcanique", "Cela semble être un simple oeuf, mais c’est en réalité une relique précieuse d’avant la naissance de Hallownest !", value=3999)

        howling_cliffs.inventory[journal_vagabond_1.name] = journal_vagabond_1
        fog_canyon.inventory[journal_vagabond_2.name] = journal_vagabond_2
        crystal_peak.inventory[journal_vagabond_3.name] = journal_vagabond_3


        crystal_peak.inventory[minerai_pale_1.name] = minerai_pale_1
        deepnest.inventory[minerai_pale_2.name] = minerai_pale_2

        crystal_peak.inventory[cle_marchand.name] = cle_marchand

        greenpath.inventory[sceau_hallownest_1.name] = sceau_hallownest_1
        self.forgotten_crossroads.inventory[sceau_hallownest_2.name] = sceau_hallownest_2
        fungal_wastes.inventory[sceau_hallownest_3.name] = sceau_hallownest_3

        fog_canyon.inventory[trampass.name] = trampass
        
        city_of_tears.inventory[idole_roi_1.name] = idole_roi_1
        mantis_village.inventory[idole_roi_2.name] = idole_roi_2

        deepnest.inventory[oeuf_arcanique.name] = oeuf_arcanique

        #Setup PNJ
            #pnj pacifique

        sly = Character( "Sly", "Un insecte replié sur lui-même, marmonnant des paroles incohérentes.", self.forgotten_crossroads, [ "…hein ?", "Laisse-moi tranquille…", "Je ne me souviens de rien…" ], merchant=False, stock={} )
        self.characters.append(sly)

        lemm = Character("Lemm","Un chercheur de reliques passionné par l'histoire du royaume.",city_of_tears, ["Je me présente en tant que Lemm, chercheurs de reliques d'Hallownest. Il existe une histoire oubliée, cachée dans les antiquités de ce royaume. Cependant, rares sont ceux qui sont disposés à s'y intéresser. Certains viennent juste pour dénicher des trésors dans les fissures et dans les ruines",
                                                                                                                "Si tu trouves une sorte de journal, celui ci offre un aperçu intéressant dans l'esprit et le coeur de ceux qui ont vécu avant nous. Je pourrais vous l'acheter contre quelques Geo","Les sceaux ornés étaient les symboles officiels du roi et de ses chevaliers, et chéris par ceux qui les portaient. Je vous en offrirai une modeste somme en échange.",
                                                                                                                "Il existe des idoles du roi d'Hallownest qui était vénéré à la fois comme un dieu et un souverain. Fabriquées à partir d'un matériau blanc mystérieux, celles-ci sont rares et très précieuses. Si vous me les vendez, je vous offrirai une bonne somme de Geo en échange.",
                                                                                                                "Il existe dans les profondeurs du royaume un oeuf qui parait simple. Mais c'est en fait, une précieuse relique qui remonte bien avant l'existence d'Hallownest ! Je vous en donnerai une petite fortune. Vendez-le-moi s'il vous plaît."], merchant=True)
        self.characters.append(lemm)

        forgeron = Character("Forgeron","Un forgeron en quête à la forge de l'aiguillon pur.", fungal_wastes, ["Mon aiguille est émoussée... tout comme ce royaume","Apporte-moi 1500 Geo et un minerai pale, et je rendrai ton aiguillon digne d'un véritable guerrier."], blacksmith=True, upgrade_cost=1500)
        self.characters.append(forgeron)

        elderbug = Character("Elderbug","Un des rares résident de Dirtmouth, il a l'air vieux et sage.", self.dirtmouth, ["J’ai bien peur qu’il ne reste plus que moi pour t’accueillir. Notre ville est devenue très silencieuse au fil du temps. Tous les autres résidents ont disparu.","Je suis Elderbug. Si tu as besoin d’aide, n’hésite pas à me parler.","Si tu cherches un marchand, tu le trouveras souvent aux Routes Oubliées ou à Dirtmouth. Il s’appelle Sly."], trainer=False)
        self.characters.append(elderbug)

        monomon = Character("Monomon l'érudite","Soudain, un air très familier frappe Quirrel lorsqu'il aperçoit la Rêveuse face à lui.", fog_canyon, ["…Quirrel. Ton esprit n'est plus lié aux chaînes d'autrefois, et pourtant tu es revenu jusqu'à moi.",
                                                                                                                                                        "Le masque que tu portes n'est plus un sceau, mais un souvenir. Un fragment de ce que tu étais.",
                                                                                                                                                        "Je t'ai confié mon savoir pour que tu marches librement, loin du poids des Rêveurs.",
                                                                                                                                                        "Le chemin que tu as suivi te ramène ici, mais le choix t'appartient désormais.",
                                                                                                                                                        "Souviens-toi : la connaissance éclaire, mais elle n'absout pas."])
        self.characters.append(monomon)

        sheo = Character("Sheo","Un insecte robuste muni d'un pinceau. Sa technique semble être celle d'une entaille implacable.", deepnest, ["Oh ! Un Visiteur ? Voilà qui rompt la monotonie.","Le combat est un art. Chaque mouvement doit être peint avec intention.","Manie ton aiguillon comme un pinceau."], trainer=True, training_cost=1000)
        self.characters.append(sheo)

        oro = Character("Oro","Un insecte robuste muni d'un aiguillon énorme. Sa technique semble être celle d'une entaille rapide comme l'éclair.", crystal_peak, ["Ne perds pas de temps. L'hésitation est une faiblesse.","La vitesse est la clé de la survie.","Si tu veux apprendre, je te montrerais mon mouvement, la Coupe de Dash."], trainer=True, training_cost=3000)
        self.characters.append(oro)

        mato = Character("Mato","Un insecte robuste muni d'un aiguillon énorme. Sa technique semble être celle d'une entaille circulaire.", blue_lake, ["La force brute ne suffit pas.","Observe ton ennemi, puis frappe là où il ne s'y attend pas.","ma technique, le Cyclone Slash, balaie tout sur son passage."], trainer=True, training_cost=5000)
        self.characters.append(mato)

        self.zote = Character("Zote", "L'incroyable et redoutable Zote se dresse devant vous ! Rare sont les créatures aussi faible que lui.", self.dirtmouth, [
    "Précepte Un : 'Gagne toujours tes combats'. Perdre un combat ne te rapporte rien et ne t'apprend rien. Gagne tes combats, ou ne t'y engage pas du tout !",
    "Précepte Deux : 'Ne les laisse jamais se moquer de toi'. Les imbéciles rient de tout, même de leurs supérieurs. Mais attention, le rire n'est pas inoffensif ! Le rire se répand comme une maladie, et bientôt tout le monde se moque de toi. Tu dois frapper à la source de cette joie perverse rapidement pour l'empêcher de se propager.",
    "Précepte Trois : 'Sois toujours reposé'. Se battre et partir à l'aventure mettent ton corps à rude épreuve. Quand tu te reposes, ton corps se renforce et se répare. Plus tu te reposes, plus tu deviens fort.",
    "Précepte Quatre : 'Oublie ton passé'. Le passé est douloureux, et penser à ton passé ne peut que t'apporter de la misère. Pense à autre chose à la place, comme l'avenir, ou de la nourriture.",
    "Précepte Cinq : 'La force bat la force'. Ton adversaire est fort ? Peu importe ! Surpasse simplement sa force avec encore plus de force, et il sera bientôt vaincu.",
    "Précepte Six : 'Choisis ton propre destin'. Nos aînés enseignent que notre destin est choisi pour nous avant même notre naissance. Je ne suis pas d'accord.",
    "Précepte Sept : 'Ne pleure pas les morts'. Quand on meurt, est-ce que les choses s'améliorent pour nous ou empirent ? Il n'y a aucun moyen de le savoir, donc on ne devrait pas s'embêter à pleurer. Ou à célébrer d'ailleurs.",
    "Précepte Huit : 'Voyage seul'. Tu ne peux compter sur personne, et personne ne sera toujours loyal. Par conséquent, personne ne devrait être ton compagnon constant.",
    "Précepte Neuf : 'Garde ta maison en ordre'. Ta maison est l'endroit où tu gardes ta possession la plus précieuse - toi-même. Par conséquent, tu devrais faire un effort pour la garder belle et propre.",
    "Précepte Dix : 'Garde ton arme affûtée'. Je m'assure que mon arme, 'Fin de Vie', est toujours bien affûtée. Cela facilite beaucoup la coupe des choses.",
    "Précepte Onze : 'Les mères te trahiront toujours'. Ce précepte s'explique de lui-même.",
    "Précepte Douze : 'Garde ton manteau au sec'. Si ton manteau est mouillé, sèche-le dès que tu peux. Porter des manteaux mouillés est désagréable et peut entraîner des maladies.",
    "Précepte Treize : 'N'aie jamais peur'. La peur ne peut que te retenir. Affronter tes peurs peut être un effort énorme. Par conséquent, tu ne devrais tout simplement pas avoir peur en premier lieu.",
    "Précepte Quatorze : 'Respecte tes supérieurs'. Si quelqu'un est ton supérieur en force ou en intelligence ou les deux, tu dois lui montrer ton respect. Ne l'ignore pas et ne te moque pas de lui.",
    "Précepte Quinze : 'Un ennemi, un coup'. Tu ne devrais utiliser qu'un seul coup pour vaincre un ennemi. Plus, c'est du gaspillage. De plus, en comptant tes coups pendant que tu te bats, tu sauras combien d'ennemis tu as vaincus.",
    "Précepte Seize : 'N'hésite pas'. Une fois que tu as pris une décision, exécute-la et ne regarde pas en arrière. Tu réussiras beaucoup plus de choses de cette façon.",
    "Précepte Dix-sept : 'Crois en ta force'. D'autres peuvent douter de toi, mais il y a quelqu'un en qui tu peux toujours avoir confiance. Toi-même. Assure-toi de croire en ta propre force, et tu ne faibliras jamais.",
    "Précepte Dix-huit : 'Cherche la vérité dans l'obscurité'. Ce précepte s'explique également de lui-même.",
    "Précepte Dix-neuf : 'Si tu essaies, réussis'. Si tu vas tenter quelque chose, assure-toi de le réussir. Si tu ne réussis pas, alors tu as en fait échoué ! Évite cela à tout prix.",
    "Précepte Vingt : 'Ne dis que la vérité'. Lorsque tu parles à quelqu'un, il est courtois et aussi efficace de parler honnêtement. Méfie-toi cependant, car parler honnêtement peut te faire des ennemis. C'est quelque chose que tu devras supporter.",
    "Précepte Vingt et un : 'Sois conscient de ton environnement'. Ne te contente pas de marcher en regardant le sol ! Tu dois lever les yeux de temps en temps, pour t'assurer que rien ne te prend par surprise.",
    "Précepte Vingt-deux : 'Abandonne le nid'. Dès que j'ai pu, j'ai quitté mon lieu de naissance et je me suis frayé un chemin dans le monde. Ne traîne pas dans le nid. Il n'y a rien pour toi là-bas.",
    "Précepte Vingt-trois : 'Identifie le point faible de l'ennemi'. Chaque ennemi que tu rencontres a un point faible, comme une fissure dans sa carapace ou le fait d'être endormi. Tu dois être constamment vigilant et scruter ton ennemi pour détecter sa faiblesse !",
    "Précepte Vingt-quatre : 'Frappe le point faible de l'ennemi'. Une fois que tu as identifié le point faible de ton ennemi, comme le précepte précédent, frappe-le. Cela les détruira instantanément.",
    "Précepte Vingt-cinq : 'Protège ton propre point faible'. Sache que ton ennemi essaiera d'identifier ton point faible, tu dois donc le protéger. La meilleure protection ? Ne jamais avoir de point faible en premier lieu.",
    "Précepte Vingt-six : 'Ne fais pas confiance à ton reflet'. En regardant certaines surfaces brillantes, tu peux voir une copie de ton propre visage. Le visage imitera tes mouvements et semble similaire au tien, mais je ne pense pas qu'on puisse lui faire confiance.",
    "Précepte Vingt-sept : 'Mange autant que tu peux'. Lorsque tu prends un repas, mange autant que tu peux. Cela te donne de l'énergie supplémentaire et signifie que tu peux manger moins souvent.",
    "Précepte Vingt-huit : 'Ne regarde pas dans l'obscurité'. Si tu regardes dans l'obscurité et que tu ne peux rien voir pendant trop longtemps, ton esprit commencera à s'attarder sur de vieux souvenirs. Les souvenirs sont à éviter, comme le précepte quatre.",
    "Précepte Vingt-neuf : 'Développe ton sens de l'orientation'. Il est facile de se perdre en voyageant à travers des cavernes sinueuses et sinueuses. Avoir un bon sens de l'orientation, c'est comme avoir une carte magique à l'intérieur de ta tête. Très utile.",
    "Précepte Trente : 'N'accepte jamais une promesse'. Rejette les promesses des autres, car elles sont toujours rompues. Les promesses d'amour ou de fiançailles sont à éviter en particulier.",
    "Précepte Trente et un : 'La maladie vit à l'intérieur de la saleté'. Tu tomberas malade si tu passes trop de temps dans des endroits sales. Si tu séjournes chez quelqu'un d'autre, exige le plus haut niveau de propreté de ton hôte.",
    "Précepte Trente-deux : 'Les noms ont du pouvoir'. Les noms ont du pouvoir, et donc nommer quelque chose, c'est lui accorder du pouvoir. J'ai moi-même nommé mon clou 'Fin de Vie'. Ne vole pas le nom que j'ai inventé ! Invente le tien !",
    "Précepte Trente-trois : 'Ne montre aucun respect à l'ennemi'. Être galant envers tes ennemis n'est pas une vertu ! Si quelqu'un s'oppose à toi, il ne mérite ni respect, ni gentillesse, ni miséricorde.",
    "Précepte Trente-quatre : 'Ne mange pas immédiatement avant de dormir'. Cela peut provoquer de l'agitation et de l'indigestion. C'est juste du bon sens.",
    "Précepte Trente-cinq : 'En haut, c'est en haut, en bas, c'est en bas'. Si tu tombes dans l'obscurité, il peut être facile de perdre ton orientation et d'oublier quel est le haut. Garde ce précepte à l'esprit !",
    "Précepte Trente-six : 'Les coquilles d'œufs sont fragiles'. Encore une fois, ce précepte s'explique de lui-même.",
    "Précepte Trente-sept : 'Emprunte, mais ne prête pas'. Si tu prêtes et que tu es remboursé, tu ne gagnes rien. Si tu empruntes mais ne rembourses pas, tu gagnes tout.",
    "Précepte Trente-huit : 'Méfie-toi de la force mystérieuse'. Une force mystérieuse pèse sur nous d'en haut, nous poussant vers le bas. Si tu passes trop de temps en l'air, la force t'écrasera contre le sol et te détruira. Méfiez-vous !",
    "Précepte Trente-neuf : 'Mange vite et bois lentement'. Ton corps est une chose délicate et tu dois l'alimenter avec une grande délibération. La nourriture doit entrer le plus vite possible, mais les liquides à un rythme plus lent.",
    "Précepte Quarante : 'N'obéis à aucune loi sauf la tienne'. Les lois écrites par d'autres peuvent t'incommoder ou être un fardeau. Que tes propres désirs soient la seule loi.",
    "Précepte Quarante et un : 'Apprends à détecter les mensonges'. Quand les autres parlent, ils mentent généralement. Scrute-les et interroge-les sans relâche jusqu'à ce qu'ils révèlent leur tromperie.",
    "Précepte Quarante-deux : 'Dépense des Geo quand tu en as'. Certains s'accrocheront à leurs Geo, les emmenant même dans la saleté avec eux lorsqu'ils mourront. Il est préférable de les dépenser quand tu peux, afin que tu puisses profiter de diverses choses dans la vie.",
    "Précepte Quarante-trois : 'Ne pardonne jamais'. Si quelqu'un te demande pardon, par exemple un de tes frères, refuse-le toujours. Ce frère, ou qui que ce soit, ne mérite pas une telle chose.",
    "Précepte Quarante-quatre : 'Tu ne peux pas respirer l'eau'. L'eau est rafraîchissante, mais si tu essaies de la respirer, tu auras une mauvaise surprise.",
    "Précepte Quarante-cinq : 'Une chose n'est pas une autre'. Celui-ci devrait être évident, mais j'ai vu d'autres essayer de soutenir qu'une chose, qui est clairement ce qu'elle est et pas autre chose, est en fait une autre chose, ce qu'elle n'est pas. Sois sur tes gardes !",
    "Précepte Quarante-six : 'Le monde est plus petit que tu ne le penses'. Quand tu es jeune, tu as tendance à penser que le monde est vaste, immense, gigantesque. C'est tout à fait naturel. Malheureusement, il est en fait beaucoup plus petit que ça. Je peux le dire, maintenant que j'ai voyagé partout dans le pays.",
    "Précepte Quarante-sept : 'Fabrique ta propre arme'. Seul toi sais exactement ce qui est nécessaire dans ton arme. J'ai moi-même fabriqué 'Fin de Vie' à partir de bois de coquille à un jeune âge. Elle ne m'a jamais fait défaut. Ni moi elle.",
    "Précepte Quarante-huit : 'Fais attention au feu'. Le feu est une sorte d'esprit chaud qui danse sans réfléchir. Il peut te réchauffer et fournir de la lumière, mais il te brûlera aussi la carapace s'il s'approche trop.",
    "Précepte Quarante-neuf : 'Les statues sont insignifiantes'. Ne les honore pas ! Personne n'a jamais fait de statue de toi ou de moi, alors pourquoi devrions-nous leur prêter attention ?",
    "Précepte Cinquante : 'Ne t'attarde pas sur les mystères'. Certaines choses dans ce monde nous apparaissent comme des énigmes. Ou des énigmes. Si le sens de quelque chose n'est pas immédiatement évident, ne perds pas de temps à y penser. Passe juste à autre chose.",
    "Précepte Cinquante et un : 'Rien n'est inoffensif'. Si on lui en donne l'occasion, tout dans ce monde te fera du mal. Amis, ennemis, monstres, chemins inégaux. Méfie-toi de tous.",
    "Précepte Cinquante-deux : 'Méfie-toi de la jalousie des pères'. Les pères croient que parce qu'ils nous ont créés, nous devons les servir et ne jamais dépasser leurs capacités. Si tu souhaites forger ton propre chemin, tu dois vaincre ton père. Ou simplement l'abandonner.",
    "Précepte Cinquante-trois : 'Ne vole pas les désirs des autres'. Chaque créature garde ses désirs enfermés en elle-même. Si tu aperçois les désirs d'un autre, résiste à l'envie de les revendiquer comme les tiens. Cela ne te mènera pas au bonheur.",
    "Précepte Cinquante-quatre : 'Si tu enfermes quelque chose, garde la clé'. Rien ne devrait être enfermé pour toujours, alors garde tes clés. Tu reviendras éventuellement et déverrouilleras tout ce que tu as caché.",
    "Précepte Cinquante-cinq : 'Ne t'incline devant personne'. Il y a dans ce monde ceux qui voudraient imposer leur volonté aux autres. Ils revendiquent la propriété de ta nourriture, de ta terre, de ton corps et même de tes pensées ! Ils n'ont rien fait pour gagner ces choses. Ne t'incline jamais devant eux et assure-toi de désobéir à leurs ordres.",
    "Précepte Cinquante-six : 'Ne rêve pas'. Les rêves sont des choses dangereuses. Des idées étranges, qui ne sont pas les tiennes, peuvent se faufiler dans ton esprit. Mais si tu résistes à ces idées, la maladie ravagera ton corps ! Mieux vaut ne pas rêver du tout, comme moi.",
    "Précepte Cinquante-sept : 'Obéis à tous les préceptes'. Plus important encore, tu dois mémoriser tous ces préceptes et leur obéir sans faillir. Y compris celui-ci ! Hmm. As-tu vraiment écouté tout ce que j'ai dit ? Recommençons et répétons les 'Cinquante-sept préceptes de Zote'"
]
)
        self.characters.append(self.zote)

            #pnj hostile
        
        hollow_knight = Character("Hollow Knight","Il a été choisi il y a fort longtemps pour sceller la Radiance… Ce vaisseau était autrefois fils du roi et de la reine d'Hallownest.", temple_black_egg, ["..."], level=14,hostile=True,is_boss=True)
        self.characters.append(hollow_knight)

        uumuu = Character("Uumuu","Une énorme méduse infecté par la Radiance. Il semble être le défenseur de la chambre de stase de Monomon.", fog_canyon, ["..."], level=10,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(uumuu)

        soul_master = Character("Le Maitre de l'ame","Chef du Sanctuaire de l'âme dans la cité des larmes, il menait des expériences sur l'Ame pour trouver un autre moyen de repousser l'infection de la Radiance. Cela a échoué à priori…", city_of_tears, ["a faire"], level=12,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(soul_master)

        hornet = Character("Hornet","Une voyageuse habile qui manie un aiguillon et un fil. Elle abat tout ce qui ce trouve sur son chemin.", greenpath, ["Recule. Ce territoire n'est pas le tien.",
                                                                                                                                                            "Tu avances trop librement pour quelqu'un qui devrait se souvenir de son rôle.",
                                                                                                                                                            "Ton masque… je reconnais son origine. Et cela me déplaît.",
                                                                                                                                                            "Les échecs du passé ne doivent pas se répéter. Je ne te laisserai pas interférer.",
                                                                                                                                                            "Si tu fais un pas de plus, je t'arrêterai moi-même."], level=3,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(hornet)

        mantis_lord = Character("Dames Mantes","Trois sœurs Mante qui siègent chacune sur trois trônes. Leur coordination est redoutable et en font un ennemi coriace.", mantis_village, ["Étranger… tu as foulé un sol que peu d’âmes osent approcher.",
                                                                                                                                                                                           "Nous sommes les gardiennes de ce village. Ici, la faiblesse n’a pas sa place.",
                                                                                                                                                                                             "Si tu avances, ce ne sera pas par la ruse ou la parole… mais par l’acier.",
                                                                                                                                                                                               "Prouve ta valeur, ou tombe comme les autres.",
                                                                                                                                                                                                 "Que le combat décide de ton droit à poursuivre ta route."],
                                                                                                                                                                                                   level=5,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(mantis_lord)

        crystal_guardian = Character("Gardien de cristal","Un ancien protecteur des mines de cristal, maintenant corrompu par l'infection.", crystal_peak, ["..."], level=2,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(crystal_guardian)

        false_knight = Character("Faux Chevalier","Un ver rendu fou par une force étrange. Il vit dans une carapace cuirassée qu’il a volé.", self.forgotten_crossroads, ["..."], level=1,hostile=True,is_boss=True ,reward_geos=500)
        self.characters.append(false_knight)

        mawlek = Character("Mawlek Maussade","Une bête féroce, mais extrêmement sociale. Elle devient agressive si elle ne peut pas s'amuser avec ceux de son espèce.", howling_cliffs, ["..."], level=4,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(mawlek)

        nosk = Character("Nosk","Un prédateur métamorphe qui imite la forme de ses proies pour les attirer dans des embuscades.", deepnest, ["..."], level=9,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(nosk)

        elder_hu = Character("Hu L'Ancien","Un rêve persistant, appartenant à un guerrier mort. Il a voyagé partout dans ce monde et s’est occupé de ceux affectés par ce fléau.", fungal_wastes, ["..."], level=7,hostile=True,is_boss=True,reward_geos=500)
        self.characters.append(elder_hu)



        # Setup player and starting room

        self.player = Player("Quirrel")
        self.player.current_room = howling_cliffs
        self.player.game = self

        #item de départ dans l'inventaire du joueur
        self.player.inventory[masque_erudite.name] = masque_erudite
        self.player.inventory[aiguillon.name] = aiguillon

        # Setup quests
        self._setup_quests()

        # Porte entre Black Egg Temple et Blue Lake
        door_tram = Door(destination=blue_lake, locked=True,key=trampass)
        temple_black_egg.exits['E'] = door_tram
        door_tram_back = Door(destination=temple_black_egg, locked=False)
        blue_lake.exits['O'] = door_tram_back
        # Gestion directions et directions inconnues

        self.direction_up = {'Haut', 'HAUT','haut','H','h','UP', 'U','Up','up','u'}
        self.direction_down = {'Bas','BAS','B','b','bas','DOWN','down','Down','D','d'}
        self.direction_west = {'Gauche','GAUCHE','gauche','G','g','Ouest','OUEST','ouest','O','o'}
        self.direction_east = {'Droite','DROITE','droite','D','d','EST','Est','est','e','E'}

    def _setup_quests(self):
        """Initialize all quests."""
        #Quête d'item : récupérer la clé du marchand
        quest_cle = Quest(
            title="cle du marchand",
            description="Sly a perdu sa clé. Retrouvez-la au sommet du royaume.",
            objectives=["prendre cle du marchand et lui vendre"],
            reward="Boutique de Sly débloquée"
        )

        #Quête déplacement,combat, intéraction : Uumuu et Monomon (good ending)
        quest_monomon = Quest(
            title="débloquer Monomon",
            description="Atteignez Fog Canyon, vianquez Uumuu et parlez à Monomon.",
            objectives=["Visiter Fog Canyon",
                        "vaincre Uumuu",
                        "parler à Monomon l'érudite"],
            reward="Personnage de Monomon débloquée"
        )

        # Quête intéraction : s'entraîner chez les 3 frères
        quest_freres = Quest(
            title="les trois frères d'aiguillon",
            description="Trouvez les trois frères et parlez-leur pour progresser dans l'art de l'aiguillon.",
            objectives=["parler à Oro",
                        "parler à Mato",
                        "parler à Sheo",],
            reward="Maîtrise de l'aiguillon augmentée"
        )

        # Quête d'item : l'oeuf arcanique (Lemm)
        quest_oeuf = Quest(
            title="oeuf arcanique",
            description="Lemm est à la recherche d'une relique précieuse : un oeuf arcanique caché dans les profondeurs.",
            objectives=["prendre oeuf arcanique",
                        "parler à Lemm"],
            reward="Connaissances du Roi Pale"
        )

        # Quête d'item : minerais pales (Forgeron)
        quest_minerais = Quest(
            title="minerais pales",
            description="Trouvez les minerais pales dans les profondeurs et apportez-les au forgeron.",
            objectives=["prendre minerai pale 1",
                        "prendre minerai pale 2",
                        "parler à Forgeron"],
            reward="Arme améliorée"
        )


        # Add quests to player's quest manager
        self.player.quest_manager.add_quest(quest_cle)
        self.player.quest_manager.add_quest(quest_monomon)
        self.player.quest_manager.add_quest(quest_freres)
        self.player.quest_manager.add_quest(quest_oeuf)
        self.player.quest_manager.add_quest(quest_minerais)
    
    #débloquer la porte de Temple of the Black Egg si toutes les quetes sont complétées
    def unlock_temple_black_egg(self):
        for room in self.rooms:
            for direction, exit_room in room.exits.items():
                if isinstance(exit_room, Door) and exit_room.destination.name == "Temple of the Black Egg": 
                    if not exit_room.locked:
                        return False
                        
                    for quest in self.player.quest_manager.quests:
                        if not quest.is_completed:
                            return False

                    exit_room.locked = False
                    print("\nLa porte du Temple de l'Œuf Noir s'est déverrouillée !\n")
                    return True
        return False    

    # Play the game
    def play(self):
        """Main game loop."""

        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
            self.unlock_temple_black_egg()

            # Check win/loose conditions
            if self.loose():
                print("\nVous êtes mort... Quirrel a été vaincu.\n")
                self.finished = True
            
            if self.win():
                print("\nFélicitations ! Vous avez vaincu Le Hollow Knight et sauvé le royaume d'Hallownest !\n")
                self.finished = True
            while not self.finished:
                command = input("> ")
                self.process_command(command)

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        """Process the command entered by the player."""
        # Split the command string into a list of words
        list_of_words = command_string.split(" ")
        command_word = list_of_words[0]


        if command_word not in self.commands.keys():
            if command_word == "":
                print(f">")
            else:
                print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")

        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nVous incarnerez {self.player.name}, un insecte amnésique provenant d'une contrée lointaine.\nCependant, votre masque, le masque de l'érudit, vous a guidé jusqu'au royaume mourant d'Hallownest. Est-ce une coïncidence ?")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())

    def get_characters_in_room(self):
        room = self.player.current_room
        return [c for c in self.characters if c.current_room == room]
    
    def win(self):
        """
        Retourne True si Le Hollow Knight a été vaincu.
        """
        for c in self.characters:
            if c.name == "Le Hollow Knight":
                return c.defeated
        return False

    def loose(self):
        """
        Retourne True si le joueur est mort(perdre un combat contre un ennemi plus fort).
        """
        return not self.player.alive

    def move_zote_randomly(self):
        """Fait se déplacer Zote aléatoirement entre Forgotten Crossroads et Dirtmouth."""
        if not hasattr(self, "zote"):
            return

        zote = self.zote

        # Zote ne bouge que s'il est dans l'une des deux zones
        if zote.current_room not in (self.forgotten_crossroads, self.dirtmouth):
            return

        # Une chance sur deux de bouger
        if random.choice([True, False]):
            # Choisir l'autre salle
            next_room = (
                self.dirtmouth
                if zote.current_room == self.forgotten_crossroads
                else self.forgotten_crossroads
            )
            zote.current_room = next_room



def main():
    
    Game().play()

    
if __name__ == "__main__":
    main()
#test