import phylib;
import os;
import sqlite3;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_OBJECTS;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
FRAME_RATE = 0.01;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> <svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";


# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg( self ):
        col = BALL_COLOURS[self.obj.still_ball.number]
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, col)
        # where cx and cy are the pos of the Ball, r is the BALL_RADIUS, and fill is the appropriate value from BALL_COLOURS.

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc ):
        """
        Constructor function. Requires ball number, position (x,y), velocity and acceleration as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    def svg( self ):
        col = BALL_COLOURS[self.obj.rolling_ball.number]
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, col)
        # where cx and cy are the pos of the Ball, r is the BALL_RADIUS, and fill is the appropriate value from BALL_COLOURS.

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0);
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole;

    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" %(self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        # where cx and cy are the pos of the Hole, and r is the HOLE_RADIUS.

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python Hcushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires ball number and position y as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion;

    def svg( self ):
        y = -25 if self.obj.hcushion.y == 0 else 2700
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" %(y)
        # where y is -25 if the cushion is at the top and y is 2700 if the cushion is at bottom.

################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires ball position x as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion;

    def svg( self ):
        x = -25 if self.obj.vcushion.x == 0 else 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)
        # where x is -25 if the cushion is on the left and x is 1350 if the cushion is at the right.


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg( self ):
        tableString = HEADER

        for obj in self:
            if obj is not None:
                tableString += obj.svg()

        tableString += FOOTER
        return tableString


    # add the roll method here
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0), 
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;

            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x, 
                                                ball.obj.still_ball.pos.y ) );

                # add ball to table
                new += new_ball;

        # return table
        return new;

    def cueBall(self):

        for ball in self:
            if ball.number == 0:
                return ball
        return None

   
# add the Database class here

class Database( ):

    def __init__( self, reset=False ):

        #If reset is set to True, it should first delete the file
        if os.path.exists( 'phylib.db' ):
            os.remove( 'phylib.db' )

        #create/open a database connection to a file in the local directory
        self.connection = sqlite3.connect( 'phylib.db' )
        self.createDB()

    def createDB(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ball(
                BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                BALLNO INTEGER NOT NULL,
                XPOS FLOAT NOT NULL,
                YPOS FLOAT NOT NULL,
                XVEL FLOAT,
                YVEL FLOAT
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TTable(
                TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                TIME FLOAT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BallTable(
                BALLID INTEGER NOT NULL,
                TABLEID INTEGER NOT NULL,
                FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Shot(
                SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                PLAYERID INTEGER NOT NULL,
                GAMEID INTEGER NOT NULL,
                FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TableShot(
                TABLEID INTEGER NOT NULL,
                SHOTID INTEGER NOT NULL,
                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Game(
                GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMENAME VARCHAR(64) NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Player(
                PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                GAMEID INTEGER NOT NULL,
                PLAYERNAME VARCHAR(64) NOT NULL,
                FOREIGN KEY (GAMEID) REFERENCES GAME(GAMEID)
            );
        ''')
        self.connection.commit()
        cursor.close()

    def readTable( self, tableID ):
        cursor = self.connection.cursor()

        table = Table()
        No = tableID + 1

        rows = []
        cursor.execute('''
            SELECT Ball.*, TTable.TIME
            FROM Ball
            INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            INNER JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
            WHERE BallTable.TABLEID = ?
        ''',(No,))

        rows = cursor.fetchall()
        
        cursor.execute('''
            SELECT * FROM TTable WHERE (TTable.TABLEID = ?);
        ''',(No,))

        if rows:
            table.time = rows[0][-1]

        for i in range(0, len(rows)):
            if rows[i][4] == 0 and rows[i][5] == 0:
                XPOS = rows[i][2]
                YPOS = rows[i][3]
                s_coo = Coordinate(XPOS, YPOS)
                sb = StillBall(rows[i][1], s_coo)
                table.__iadd__(sb)

            else:
                XPOS = rows[i][2]
                YPOS = rows[i][3]
                XVEL = rows[i][4]
                YVEL = rows[i][5]
                r_coo = Coordinate(XPOS, YPOS)
                r_vel = Coordinate(XVEL, YVEL)
                r_acc = Coordinate(-DRAG * XVEL / phylib.phylib_length(Coordinate(XVEL, YVEL)) , -DRAG * YVEL / phylib.phylib_length(Coordinate(XVEL, YVEL)))

                rb = RollingBall(rows[i][1], r_coo, r_vel, r_acc)
                table.__iadd__(rb)
        self.connection.commit()
        cursor.close()

        return table

    def writeTable( self, table):

        cursor = self.connection.cursor()
        balls = []
        #table = Table()
        j = 10

        while iter(table) is not None and j < MAX_OBJECTS:

            if isinstance(table[j], StillBall):
                cursor.execute('''
                    INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, 0.0, 0.0);
                ''',(table[j].obj.still_ball.number, table[j].obj.still_ball.pos.x, table[j].obj.still_ball.pos.y))
            elif isinstance(table[j], RollingBall):
                cursor.execute('''
                    INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?);
                ''',(table[j].obj.rolling_ball.number, table[j].obj.rolling_ball.pos.x, table[j].obj.rolling_ball.pos.y, table[j].obj.rolling_ball.vel.x, table[j].obj.rolling_ball.vel.y))

            cursor.execute('''
                SELECT BALLID FROM Ball WHERE BALLID = last_insert_rowid();
            ''')

            reel = cursor.fetchone()
            if reel is not None:
                balls.append(reel[0]) 

            j = j + 1

        cursor.execute('''
            INSERT INTO TTable (TIME) VALUES (%f);
        '''%table.time)

        cursor.execute('''
            SELECT TABLEID FROM TTable
            WHERE TABLEID = last_insert_rowid(); 
        ''')

        TABLEID = (cursor.fetchone())[0]
        cursor.fetchall()

        #adding ballid and table id into ball table 
        for n in range(0, len(balls)):
            cursor.execute('''
                INSERT INTO BallTable VALUES (?, ?);
            ''',(balls[n], TABLEID))

        self.connection.commit()
        cursor.close()
        return TABLEID -1


    def close( self ):
        if self.connection:
            self.connection.commit()
            self.connection.close()


    def getGame(self, gameID):

        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT Game.GAMENAME, player1.PLAYERNAME, player2.PLAYERNAME
            FROM Game
            JOIN Player player1 ON game.GAMEID = player1.GAMEID AND player1.PLAYERID = (
                SELECT MIN(PLAYERID) FROM Player WHERE GAMEID = game.GAMEID
            )
            JOIN Player player2 ON game.GAMEID = player2.GAMEID AND player2.PLAYERID != player1.PLAYERID
            WHERE game.GAMEID = ?;
        ''',(gameID,))

        #game_info = self.cursor.fetchone()
        #if game_info:
        #    gameName, player1Name, player2Name = game_info
        #    return gameName, player1Name, player2Name
        return cursor.fetchall()

    def setGame(self, gameName, player1Name, player2Name):

        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO Game (GAMENAME) VALUES (?);
        ''',(gameName,))

        cursor.execute('''
            SELECT GAMEID FROM Game WHERE GAMEID = last_insert_rowid();
        ''')
        gameID = (cursor.fetchone()[0])
        cursor.fetchall()
        #gameID = self.cursor.lastrowid

        cursor.execute('''
            INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?);
        ''',(gameID, player1Name))
        player1ID = self.cursor.lastrowid

        cursor.execute('''
            INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?);
        ''',(gameID, player2Name))
        player2ID = self.cursor.lastrowid

        self.connection.commit()
        cursor.close()
        return gameID

    def newShot(self, gameName, playerName):
        cursor = self.connection.cursor()

        # Get the GAMEID for the gameName
        cursor.execute('''
            SELECT GAMEID FROM Game WHERE GAMENAME = (?);
        ''', (gameName,))
        game_id = cursor.fetchone()[0]

        # Get the PLAYERID for the playerName
        cursor.execute('''
            SELECT PLAYERID FROM Player WHERE PLAYERNAME = (?) AND GAMEID = (?)
        ''', (playerName, game_id))
        player_id = cursor.fetchone()[0]

        # Insert the new entry for the Shot table
        cursor.execute('''
            INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)
        ''', (player_id, game_id))
        shotID = cursor.lastrowid

        self.connection.commit()
        cursor.close()

        return shotID


class Game( ):

    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):

        if gameID is not None and gameName is None and player1Name is None and player2Name is None:

            gameID = gameID + 1
            self.getGame(gameID)

        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
             
            db = Database(False)
            gameID = db.setGame(gameName, player1Name, player2Name)
            db.close()

        else:
            raise TypeError("Invalid arguments were given")

    def shoot( self, gameName, playerName, table, xvel, yvel ):

        db = Database(False)
        shotID = db.newShot(gameName, playerName)

        cue_ball = table.cueBall()

        if cue_ball:
            # Storing the cue balls position
            xpos = cue_ball.obj.still_ball.pos.x 
            ypos = cue_ball.obj.still_ball.pos.x

            # Setting the cue balls type to ROLLING_BALL
            cue_ball.type = phylib.ROLLING_BALL

        # Set cue balls attributes
        xpos = cue_ball.obj.rolling_ball.pos.x
        ypos = cue_ball.obj.rolling_ball.pos.y
        xvel = cue_ball.obj.rolling_ball.vel.x
        yvel = cue_ball.obj.rolling_ball.vel.y

        rvel = Coordinate(xvel, yvel)

        if phylib.phylib_length(velr) != 0:
            cue_ball.obj.rolling_ball.acc.x = -xvel / phylib.phylib_length(velr) * DRAG
            cue_ball.obj.rolling_ball.acc.y = -yvel / phylib.phylib_length(velr) * DRAG
        else:
            cue_ball.obj.rolling_ball.acc.x = 0
            cue_ball.obj.rolling_ball.acc.y = 0

        time = table.time
        while True:

            table = table.segment(time)
            if table is None:
                break

            # Calculating the segment time
            segmentTime = floor((table.time - time) / FRAME_RATE)

            for i in range (segmentTime):
                tempTime = i * FRAME_RATE
                newTable = table.roll(tempTime)
                newTable.time = time + tempTime
                
                tableID = db.writeTable(newTable)
                dataB.recordTableShot(tableID, shotID)

        db.close()
        
        return shotID