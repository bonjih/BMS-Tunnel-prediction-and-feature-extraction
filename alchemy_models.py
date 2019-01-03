# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, String, text
from dbconnect.base import Base


class Agency(Base):
    __tablename__ = 'agency'

    AgencyID = Column(Integer, primary_key=True)
    Agency = Column(String(45), nullable=False)


class Animal(Base):
    __tablename__ = 'animal'

    AnimalID = Column(Integer, primary_key=True)
    LogID = Column(String(10))
    AnimalType = Column(String(45))
    AnimalState = Column(String(45))



class Aordatum(Base):
    __tablename__ = 'aordata'

    AORDataID = Column(Integer, primary_key=True)
    AnimalType = Column(String(45))


class Bddatum(Base):
    __tablename__ = 'bddata'

    BDDataID = Column(Integer, primary_key=True)
    FieldType = Column(String(45), nullable=False)
    VehicleType = Column(String(45), nullable=False)
    Reason = Column(String(45), nullable=False)


class Breakdown(Base):
    __tablename__ = 'breakdowns'

    BreakdownsID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    VehicleType = Column(String(45))
    Reason = Column(String(45))


class Callout(Base):
    __tablename__ = 'callout'

    CallOutID = Column(Integer, primary_key=True)
    LogID = Column(String(10))
    Organisation = Column(String(45))
    Name = Column(String(45))
    Contact = Column(String(10))
    Arrive = Column(String(10))


class Category(Base):
    __tablename__ = 'categories'

    categoriesID = Column(Integer, primary_key=True)
    categories = Column(String(45))


class Cfvdatum(Base):
    __tablename__ = 'cfvdata'

    CFVDataID = Column(Integer, primary_key=True)
    Direction = Column(String(45), nullable=False)


class Closure(Base):
    __tablename__ = 'closures'

    CID = Column(Integer, primary_key=True)
    LogID = Column(String(12), nullable=False)
    CDirection = Column(String(32))
    CLocation = Column(String(32))
    CTCPImp = Column(DateTime)
    CTCPLifted = Column(DateTime)
    CLane = Column(String(150))
    CTCPNo = Column(String(6))
    CEndLocation = Column(String(45))
    Closure = Column(String(3), server_default=text("'0'"))


class Collector(Base):
    __tablename__ = 'collectors'

    CollectorsID = Column(Integer, primary_key=True)
    LogID = Column(String(10))
    Collector = Column(String(45))


class Collision(Base):
    __tablename__ = 'collisions'

    CollID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    Injuries = Column(String(32))
    CollType = Column(String(32))
    Chainage = Column(String(32))
    Towed = Column(String(3))
    Weather = Column(String(32))
    Damage = Column(String(3))
    Cars = Column(Integer)
    Motorcycles = Column(Integer)
    Trucks = Column(Integer)
    Buses = Column(Integer)
    Ambulance = Column(String(3))


class Config(Base):
    __tablename__ = 'config'

    ConfigID = Column(Integer, primary_key=True)
    ConfigType = Column(String(12))
    SMTPHost = Column(String(24))
    SMTPUserName = Column(String(45))
    SMTPPassword = Column(String(45))
    SMSAddress = Column(String(45))
    SMTPPort = Column(String(6))
    SMTPFromAddress = Column(String(120))
    SiteName = Column(String(45))
    ReportServer = Column(String(90))
    IRPPath = Column(String(255))
    MaximoAddress = Column(String(255))
    AffectedLength = Column(String(12))
    TotalLength = Column(String(12))
    ScreenColour = Column(String(24))


class Congestion(Base):
    __tablename__ = 'congestion'

    CongestionID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    BackTo = Column(String(45))
    CongFrom = Column(DateTime)
    CongTo = Column(DateTime)


class Contraflow(Base):
    __tablename__ = 'contraflow'

    ContraflowID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    Direction = Column(String(45))
    Evasion = Column(String(3))


class Controller(Base):
    __tablename__ = 'controllers'

    ControllerName = Column(String(32), nullable=False)
    UserName = Column(String(64), primary_key=True)
    Administrator = Column(String(3))


class Dangerousgood(Base):
    __tablename__ = 'dangerousgoods'

    DangerousgoodsID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    VehicleStop = Column(String(3))
    Goods = Column(String(45))


class Debris(Base):
    __tablename__ = 'debris'

    DebrisID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    Type = Column(String(45))
    Hazardous = Column(String(3))


class Debrisdatum(Base):
    __tablename__ = 'debrisdata'

    DebrisDataID = Column(Integer, primary_key=True)
    DebrisType = Column(String(45), nullable=False)


class Default(Base):
    __tablename__ = 'defaults'

    DefaultsID = Column(Integer, primary_key=True)
    DefEvent = Column(String(32), nullable=False, unique=True)
    DefDirection = Column(String(32))
    DefLocation = Column(String(32))
    DefSubLocation = Column(String(32))
    DefLane = Column(String(32))
    DefSource = Column(String(32))


class Dgdatum(Base):
    __tablename__ = 'dgdata'

    DGDataID = Column(Integer, primary_key=True)
    LoadContents = Column(String(45), nullable=False)


class Direction(Base):
    __tablename__ = 'direction'

    DirectionID = Column(Integer, primary_key=True)
    Direction = Column(String(45))


class Emplevel(Base):
    __tablename__ = 'emplevel'

    emplevelID = Column(Integer, primary_key=True)
    EMPLevel = Column(String(45))


class Escalate(Base):
    __tablename__ = 'escalate'

    EscalateID = Column(Integer, primary_key=True)
    ECompany = Column(String(45))
    EName = Column(String(45), nullable=False, unique=True)
    EEmail = Column(String(90), nullable=False)
    EMobile = Column(String(15))
    ESelected = Column(Integer)
    EType = Column(String(12))
    Cat1 = Column(Integer, server_default=text("'0'"))
    Cat2 = Column(Integer, server_default=text("'0'"))
    Cat3 = Column(Integer, server_default=text("'0'"))
    Maint = Column(Integer, server_default=text("'0'"))


class Holiday(Base):
    __tablename__ = 'holidays'

    HolidaysID = Column(Integer, primary_key=True)
    Holiday = Column(Date, nullable=False)


class Incidentcat(Base):
    __tablename__ = 'incidentcats'

    IncidentCatsID = Column(Integer, primary_key=True)
    IncidentType = Column(String(45))
    IncidentCat = Column(String(45))


class Incidenttype(Base):
    __tablename__ = 'incidenttype'

    IncidentType = Column(String(32), primary_key=True)
    EventType = Column(String(45))
    DefCriticality = Column(String(3))
    Reportable = Column(String(3), server_default=text("'No'"))
    SignificantEvent = Column(String(3), server_default=text("'No'"))


class Isolation(Base):
    __tablename__ = 'isolations'

    IsolationsID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    IsolationDate = Column(DateTime)
    ConfirmedBy = Column(String(32))
    Device = Column(String(45))
    Action = Column(String(24))
    Maximo = Column(String(12))
    Reason = Column(String(90))
    InService = Column(DateTime)
    InServiceBy = Column(String(32))
    RequestedBy = Column(String(45))


class Lane(Base):
    __tablename__ = 'lane'

    LaneID = Column(Integer, primary_key=True)
    Lane = Column(String(45))


class Link(Base):
    __tablename__ = 'links'

    linksID = Column(Integer, primary_key=True)
    LinkName = Column(String(45))
    LinkDestination = Column(String(255))


class Location(Base):
    __tablename__ = 'location'

    Location = Column(String(32), primary_key=True)
    LDirection = Column(String(45))


class Location(Base):
    __tablename__ = 'locations'

    LocationsID = Column(Integer, primary_key=True)
    LDirection = Column(String(45))
    Location = Column(String(45))


class Log(Base):
    __tablename__ = 'log'

    logid = Column(Integer, primary_key=True)
    IncidentDate = Column(DateTime, nullable=False)
    ControllerName = Column(String(32), nullable=False)
    IncidentType = Column(String(32), nullable=False)
    Direction = Column(String(32))
    Location = Column(String(32))
    SubLocation = Column(String(32))
    Lane = Column(String(32))
    Source = Column(String(32), nullable=False)
    Description = Column(String, nullable=False)
    IncidentDetection = Column(DateTime)
    IncidentResponse = Column(DateTime)
    ResponseDespatch = Column(DateTime)
    SDTime = Column(DateTime)
    ResponseOnsite = Column(DateTime)
    IncidentClear = Column(DateTime)
    Category = Column(String(45))
    Criticality = Column(String(3))
    Reporter = Column(String(45))
    Responder = Column(String(45))
    Closure = Column(Integer)
    Power = Column(String(3), server_default=text("'0'"))
    Parent = Column(String(10))
    MaximoNo = Column(String(12))
    TCCOLock = Column(Integer, server_default=text("'0'"))


class Notification(Base):
    __tablename__ = 'notifications'

    NotificationsID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    NAgency = Column(String(45))
    NNote = Column(String(45))
    NTime = Column(String(10))


class Notify(Base):
    __tablename__ = 'notify'

    NLogID = Column(String(12), primary_key=True)
    NDescription = Column(String)
    NResponding = Column(String(45))
    NCategory = Column(String(24))
    NClearTime = Column(String(24))
    NStatus = Column(String(24))
    FinalSMSSent = Column(Integer, server_default=text("'0'"))
    FinalMailSent = Column(Integer, server_default=text("'0'"))


class Odvdatum(Base):
    __tablename__ = 'odvdata'

    ODVDataID = Column(Integer, primary_key=True)
    LoadContents = Column(String(45), nullable=False)


class Overheight(Base):
    __tablename__ = 'overheight'

    OverheightID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    VehicleStop = Column(String(3))
    Goods = Column(String(45))


class Password(Base):
    __tablename__ = 'password'

    Password = Column(String(12), primary_key=True)


class Pddatum(Base):
    __tablename__ = 'pddata'

    PDDataID = Column(Integer, primary_key=True)
    Offender = Column(String(45), nullable=False)


class Pedestrian(Base):
    __tablename__ = 'pedestrian'

    PedestrianID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    Offender = Column(String(45))


class Responder(Base):
    __tablename__ = 'responders'

    RespondersID = Column(Integer, primary_key=True)
    Responders = Column(String(45), unique=True)


class Source(Base):
    __tablename__ = 'source'

    Source = Column(String(32), primary_key=True)


class Spawn(Base):
    __tablename__ = 'spawn'

    SpawnID = Column(Integer, primary_key=True)
    LogID = Column(String(10))
    Child = Column(String(10))


class Stationary(Base):
    __tablename__ = 'stationary'

    StationaryID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    Reason = Column(String(45))
    HazMat = Column(String(3))


class Sublocation(Base):
    __tablename__ = 'sublocation'

    SubLocationID = Column(Integer, primary_key=True)
    SubLocation = Column(String(45))


class Subloc(Base):
    __tablename__ = 'sublocs'

    SID = Column(Integer, primary_key=True)
    SLocation = Column(String(32), nullable=False)


class Svdatum(Base):
    __tablename__ = 'svdata'

    SVDataID = Column(Integer, primary_key=True)
    Reason = Column(String(45), nullable=False)


class Synopsi(Base):
    __tablename__ = 'synopsis'

    SynopsisID = Column(Integer, primary_key=True)
    LogID = Column(String(10))
    Synopsis = Column(String)
    Type = Column(String(10))
    SynopsisText = Column(String)


class Tcp(Base):
    __tablename__ = 'tcp'

    TCPNo = Column(Integer, primary_key=True, unique=True)
    TCPName = Column(String(150))
    TCPDescription = Column(String(150))
    TCPType = Column(String(45))
    TCPSubType = Column(String(45))
    TCPDirection = Column(String(12))
    TCPFrom = Column(String(45))
    TCPTo = Column(String(45))
    TCPCarriageway = Column(String(45))
    TCPLane = Column(String(45))
    TCPAPLChange = Column(String(150))
    TCPComment = Column(String(150))
    TCPLink = Column(String(6))
    TCPRevision = Column(String(45))
    TCPClosure = Column(String(3), server_default=text("'0'"))


class Vehicle(Base):
    __tablename__ = 'vehicles'

    VehiclesID = Column(Integer, primary_key=True)
    LogID = Column(String(10), nullable=False)
    VRego = Column(String(12))
    VState = Column(String(3))
    VDescription = Column(String(45))
