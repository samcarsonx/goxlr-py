from enum import Enum

# Enumerators used by the GoXLR Utility Daemon. (with slight name changes)


class PathType(Enum):
    Profiles = 1
    MicProfiles = 2
    Presets = 3
    Samples = 4
    Icons = 5
    Logs = 6


class LogLevel(Enum):
    Off = 1
    Error = 2
    Warn = 3
    Info = 4
    Debug = 5
    Trace = 6


class Channel(Enum):
    Mic = 1
    LineIn = 2
    Console = 3
    System = 4
    Game = 5
    Chat = 6
    Sample = 7
    Music = 8
    Headphones = 9
    MicMonitor = 10
    LineOut = 11


class Mix(Enum):
    A = 1
    B = 2


class SubMixChannel(Enum):
    Mic = 1
    LineIn = 2
    Console = 3
    System = 4
    Game = 5
    Chat = 6
    Sample = 7
    Music = 8


class Fader(Enum):
    A = 1
    B = 2
    C = 3
    D = 4


class Encoder(Enum):
    Pitch = 1
    Gender = 2
    Reverb = 3
    Echo = 4


class OutputDevice(Enum):
    Headphones = 1
    BroadcastMix = 2
    ChatMic = 3
    Sampler = 4
    LineOut = 5


class InputDevice(Enum):
    Microphone = 1
    Chat = 2
    Music = 3
    Game = 4
    Console = 5
    LineIn = 6
    System = 7
    Samples = 8


class EffectKey(Enum):
    DisableMic = 0x0158
    BleepLevel = 0x0073
    GateMode = 0x0010
    GateThreshold = 0x0011
    GateEnabled = 0x0014
    GateAttenuation = 0x0015
    GateAttack = 0x0016
    GateRelease = 0x0017
    MicCompSelect = 0x014B
    Equalizer31HzFrequency = 0x0126
    Equalizer31HzGain = 0x0127
    Equalizer63HzFrequency = 0x00F8
    Equalizer63HzGain = 0x00F9
    Equalizer125HzFrequency = 0x0113
    Equalizer125HzGain = 0x0114
    Equalizer250HzFrequency = 0x0129
    Equalizer250HzGain = 0x012A
    Equalizer500HzFrequency = 0x0116
    Equalizer500HzGain = 0x0117
    Equalizer1KHzFrequency = 0x011D
    Equalizer1KHzGain = 0x011E
    Equalizer2KHzFrequency = 0x012C
    Equalizer2KHzGain = 0x012D
    Equalizer4KHzFrequency = 0x0120
    Equalizer4KHzGain = 0x0121
    Equalizer8KHzFrequency = 0x0109
    Equalizer8KHzGain = 0x010A
    Equalizer16KHzFrequency = 0x012F
    Equalizer16KHzGain = 0x0130
    CompressorThreshold = 0x013D
    CompressorRatio = 0x013C
    CompressorAttack = 0x013E
    CompressorRelease = 0x013F
    CompressorMakeUpGain = 0x0140
    DeEsser = 0x000B
    ReverbAmount = 0x0076
    ReverbDecay = 0x002F
    ReverbEarlyLevel = 0x0037
    ReverbTailLevel = 0x0039  # Always sent as 0.
    ReverbPredelay = 0x0030
    ReverbLowColor = 0x0032
    ReverbHighColor = 0x0033
    ReverbHighFactor = 0x0034
    ReverbDiffuse = 0x0031
    ReverbModSpeed = 0x0035
    ReverbModDepth = 0x0036
    ReverbType = 0x002E
    EchoAmount = 0x0075
    EchoFeedback = 0x0028
    EchoTempo = 0x001F
    EchoDelayL = 0x0022
    EchoDelayR = 0x0023
    EchoFeedbackL = 0x0024
    EchoFeedbackR = 0x0025
    EchoXFBLtoR = 0x0026
    EchoXFBRtoL = 0x0027
    EchoSource = 0x001E
    EchoDivL = 0x0020
    EchoDivR = 0x0021
    EchoFilterStyle = 0x002A
    PitchAmount = 0x005D
    PitchCharacter = 0x0167
    PitchThreshold = 0x0159
    GenderAmount = 0x0060
    MegaphoneAmount = 0x003C
    MegaphonePostGain = 0x0040
    MegaphoneStyle = 0x003A
    MegaphoneHP = 0x003D
    MegaphoneLP = 0x003E
    MegaphonePreGain = 0x003F
    MegaphoneDistType = 0x0041
    MegaphonePresenceGain = 0x0042
    MegaphonePresenceFC = 0x0043
    MegaphonePresenceBW = 0x0044
    MegaphoneBeatboxEnable = 0x0045
    MegaphoneFilterControl = 0x0046
    MegaphoneFilter = 0x0047
    MegaphoneDrivePotGainCompMid = 0x0048
    MegaphoneDrivePotGainCompMax = 0x0049
    RobotLowGain = 0x0134
    RobotLowFreq = 0x0133
    RobotLowWidth = 0x0135
    RobotMidGain = 0x013A
    RobotMidFreq = 0x0139
    RobotMidWidth = 0x013B
    RobotHiGain = 0x0137
    RobotHiFreq = 0x0136
    RobotHiWidth = 0x0138
    RobotWaveform = 0x0147
    RobotPulseWidth = 0x0146
    RobotThreshold = 0x0157
    RobotDryMix = 0x014D
    RobotStyle = 0x0000
    HardTuneKeySource = 0x0059  # Always sent as 0.
    HardTuneAmount = 0x005A
    HardTuneRate = 0x005C
    HardTuneWindow = 0x005B
    HardTuneScale = 0x005E
    HardTunePitchAmount = 0x005F

    RobotEnabled = 0x014E
    MegaphoneEnabled = 0x00D7
    HardTuneEnabled = 0x00D8

    Encoder1Enabled = 0x00D5
    Encoder2Enabled = 0x00D6
    Encoder3Enabled = 0x0150
    Encoder4Enabled = 0x0151


class MicrophoneParamKey(Enum):
    MicType = 0x000
    DynamicGain = 0x001
    CondenserGain = 0x002
    JackGain = 0x003
    GateThreshold = 0x30200
    GateAttack = 0x30400
    GateRelease = 0x30600
    GateAttenuation = 0x30900
    CompressorThreshold = 0x60200
    CompressorRatio = 0x60300
    CompressorAttack = 0x60400
    CompressorRelease = 0x60600
    CompressorMakeUpGain = 0x60700
    BleepLevel = 0x70100

    """
     These are the values for the GoXLR mini, it seems there's a difference in how the two
     are setup, The Mini does EQ via mic parameters, where as the full does it via effects.
    """
    Equalizer90HzFrequency = 0x40000
    Equalizer90HzGain = 0x40001
    Equalizer250HzFrequency = 0x40003
    Equalizer250HzGain = 0x40004
    Equalizer500HzFrequency = 0x40006
    Equalizer500HzGain = 0x40007
    Equalizer1KHzFrequency = 0x50000
    Equalizer1KHzGain = 0x50001
    Equalizer3KHzFrequency = 0x50003
    Equalizer3KHzGain = 0x50004
    Equalizer8KHzFrequency = 0x50006
    Equalizer8KHzGain = 0x50007


class FaderDisplayStyle(Enum):
    TwoColour = 1
    Gradient = 2
    Meter = 3
    GradientMeter = 4


class Button(Enum):
    # These are all the buttons from the GoXLR Mini.
    Fader1Mute = 1
    Fader2Mute = 2
    Fader3Mute = 3
    Fader4Mute = 4
    Bleep = 5
    Cough = 6

    # The rest are GoXLR Full Buttons. On the mini, they will simply be ignored.
    EffectSelect1 = 7
    EffectSelect2 = 8
    EffectSelect3 = 9
    EffectSelect4 = 10
    EffectSelect5 = 11
    EffectSelect6 = 12

    # FX Button labelled as 'fxClear' in config?
    EffectFx = 13
    EffectMegaphone = 14
    EffectRobot = 15
    EffectHardTune = 16

    SamplerSelectA = 17
    SamplerSelectB = 18
    SamplerSelectC = 19

    SamplerTopLeft = 20
    SamplerTopRight = 21
    SamplerBottomLeft = 22
    SamplerBottomRight = 23
    SamplerClear = 24


class SimpleColourTarget(Enum):
    Global = 1
    Accent = 2
    Scribble1 = 3
    Scribble2 = 4
    Scribble3 = 5
    Scribble4 = 6


class SamplerColourTarget(Enum):
    SamplerSelectA = 1
    SamplerSelectB = 2
    SamplerSelectC = 3


class EncoderColourTarget(Enum):
    Reverb = 1
    Pitch = 2
    Echo = 3
    Gender = 4


class ButtonColourGroup(Enum):
    FaderMute = 1
    EffectSelector = 2
    EffectTypes = 3


class ButtonColourOffStyle(Enum):
    Dimmed = 1
    Colour2 = 2
    DimmedColour2 = 3


class MuteFunction(Enum):
    All = 1
    ToStream = 2
    ToVoiceChat = 3
    ToPhones = 4
    ToLineOut = 5


class MicrophoneType(Enum):
    Dynamic = 1
    Condenser = 2
    Jack = 3


class EffectBankPreset(Enum):
    Preset1 = 1
    Preset2 = 2
    Preset3 = 3
    Preset4 = 4
    Preset5 = 5
    Preset6 = 6


class SampleBank(Enum):
    A = 1
    B = 2
    C = 3


class MiniEqFrequency(Enum):
    Equalizer90Hz = 1
    Equalizer250Hz = 2
    Equalizer500Hz = 3
    Equalizer1KHz = 4
    Equalizer3KHz = 5
    Equalizer8KHz = 6


class EqFrequency(Enum):
    Equalizer31Hz = 1
    Equalizer63Hz = 2
    Equalizer125Hz = 3
    Equalizer250Hz = 4
    Equalizer500Hz = 5
    Equalizer1KHz = 6
    Equalizer2KHz = 7
    Equalizer4KHz = 8
    Equalizer8KHz = 9
    Equalizer16KHz = 10


class CompressorRatio(Enum):
    Ratio1_0 = 1
    Ratio1_1 = 2
    Ratio1_2 = 3
    Ratio1_4 = 4
    Ratio1_6 = 5
    Ratio1_8 = 6
    Ratio2_0 = 7
    Ratio2_5 = 8
    Ratio3_2 = 9
    Ratio4_0 = 10
    Ratio5_6 = 11
    Ratio8_0 = 12
    Ratio16_0 = 13
    Ratio32_0 = 14
    Ratio64_0 = 15


class GateTime(Enum):
    Gate10ms = 1
    Gate20ms = 2
    Gate30ms = 3
    Gate40ms = 4
    Gate50ms = 5
    Gate60ms = 6
    Gate70ms = 7
    Gate80ms = 8
    Gate90ms = 9
    Gate100ms = 10
    Gate110ms = 11
    Gate120ms = 12
    Gate130ms = 13
    Gate140ms = 14
    Gate150ms = 15
    Gate160ms = 16
    Gate170ms = 17
    Gate180ms = 18
    Gate190ms = 19
    Gate200ms = 20
    Gate250ms = 21
    Gate300ms = 22
    Gate350ms = 23
    Gate400ms = 24
    Gate450ms = 25
    Gate500ms = 26
    Gate550ms = 27
    Gate600ms = 28
    Gate650ms = 29
    Gate700ms = 30
    Gate750ms = 31
    Gate800ms = 32
    Gate850ms = 33
    Gate900ms = 34
    Gate950ms = 35
    Gate1000ms = 36
    Gate1100ms = 37
    Gate1200ms = 38
    Gate1300ms = 39
    Gate1400ms = 40
    Gate1500ms = 41
    Gate1600ms = 42
    Gate1700ms = 43
    Gate1800ms = 44
    Gate1900ms = 45
    Gate2000ms = 46


class CompressorAttackTime(Enum):
    Comp0ms = 1
    Comp2ms = 2
    Comp3ms = 3
    Comp4ms = 4
    Comp5ms = 5
    Comp6ms = 6
    Comp7ms = 7
    Comp8ms = 8
    Comp9ms = 9
    Comp10ms = 10
    Comp12ms = 11
    Comp14ms = 12
    Comp16ms = 13
    Comp18ms = 14
    Comp20ms = 15
    Comp23ms = 16
    Comp26ms = 17
    Comp30ms = 18
    Comp35ms = 19
    Comp40ms = 20


class CompressorReleaseTime(Enum):
    Comp0ms = 1
    Comp15ms = 2
    Comp25ms = 3
    Comp35ms = 4
    Comp45ms = 5
    Comp55ms = 6
    Comp65ms = 7
    Comp75ms = 8
    Comp85ms = 9
    Comp100ms = 10
    Comp115ms = 11
    Comp140ms = 12
    Comp170ms = 13
    Comp230ms = 14
    Comp340ms = 15
    Comp680ms = 16
    Comp1000ms = 17
    Comp1500ms = 18
    Comp2000ms = 19
    Comp3000ms = 20


class ReverbStyle(Enum):
    Library = 1
    DarkBloom = 2
    MusicClub = 3
    RealPlate = 4
    Chapel = 5
    HockeyArena = 6


class EchoStyle(Enum):
    Quarter = 1
    Eighth = 2
    Triplet = 3
    PingPong = 4
    ClassicSlap = 5
    MultiTap = 6


class PitchStyle(Enum):
    Narrow = 1
    Wide = 2


class GenderStyle(Enum):
    Narrow = 1
    Medium = 2
    Wide = 3


class MegaphoneStyle(Enum):
    Megaphone = 1
    Radio = 2
    OnThePhone = 3
    Overdrive = 4
    BuzzCutt = 5
    Tweed = 6


class RobotStyle(Enum):
    Robot1 = 1
    Robot2 = 2
    Robot3 = 3


class RobotRange(Enum):
    Low = 1
    Medium = 2
    High = 3


class HardTuneStyle(Enum):
    Natural = 1
    Medium = 2
    Hard = 3


class HardTuneSource(Enum):
    All = 1
    Music = 2
    Game = 3
    LineIn = 4
    System = 5


class SampleButton(Enum):
    TopLeft = 1
    TopRight = 2
    BottomLeft = 3
    BottomRight = 4


class SamplePlaybackMode(Enum):
    PlayNext = 1
    PlayStop = 2
    PlayFade = 3
    StopOnRelease = 4
    FadeOnRelease = 5
    Loop = 6


class SamplePlayOrder(Enum):
    Sequential = 1
    Random = 2


class DisplayMode(Enum):
    Simple = 1
    Advanced = 2


class DisplayModeComponent(Enum):
    NoiseGate = 1
    Equaliser = 2
    Compressor = 3
    EqFineTune = 4


class MuteState(Enum):
    Unmuted = 1
    MutedToX = 2
    MutedToAll = 3


class AnimationMode(Enum):
    RetroRainbow = 1
    RainbowDark = 2
    RainbowBright = 3
    Simple = 4
    Ripple = 5
    NONE = 6


class WaterfallDirection(Enum):
    Down = 1
    Up = 2
    Off = 3


class DeviceType(Enum):
    Unknown = 1
    Full = 2
    Mini = 3


class IDType(Enum):
    Heartbeat: int = 0
    Patch: int = 2**64 - 1


class PatchOperation(Enum):
    Add = 1
    Remove = 2
    Replace = 3
    Copy = 4
    Move = 5
    Test = 6
