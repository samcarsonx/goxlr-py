from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from .enums import *

# --------------------------------------------------
# Config
# --------------------------------------------------


@dataclass
class HttpSettings:
    enabled: bool
    bind_address: str
    cors_enabled: bool
    port: int

    def __init__(self, http_settings: dict):
        self.enabled = http_settings.get("enabled")
        self.bind_address = http_settings.get("bind_address")
        self.cors_enabled = http_settings.get("cors_enabled")
        self.port = http_settings.get("port")


@dataclass
class Config:
    http_settings: HttpSettings
    daemon_version: str
    autostart_enabled: bool
    show_tray_icon: bool
    tts_enabled: bool
    allow_network_access: bool
    log_level: LogLevel

    def __init__(self, config: dict):
        self.http_settings = HttpSettings(config.get("http_settings"))
        self.daemon_version = config.get("daemon_version")
        self.autostart_enabled = config.get("autostart_enabled")
        self.show_tray_icon = config.get("show_tray_icon")
        self.tts_enabled = config.get("tts_enabled")
        self.allow_network_access = config.get("allow_network_access")
        self.log_level = LogLevel[config.get("log_level")]


# --------------------------------------------------
# Mixer - Hardware
# --------------------------------------------------


@dataclass
class MixerVersions:
    firmware: List[int]
    fpga_count: int
    dice: List[int]

    def __init__(self, mixer_version: dict):
        self.firmware = mixer_version.get("firmware")
        self.fpga_count = mixer_version.get("fpga_count")
        self.dice = mixer_version.get("dice")


@dataclass
class USBDevice:
    manufacturer_name: str
    product_name: str
    version: List[int]
    bus_number: int
    address: int
    identifier: str

    def __init__(self, usb_device: dict):
        self.manufacturer_name = usb_device.get("manufacturer_name")
        self.product_name = usb_device.get("product_name")
        self.version = usb_device.get("version")
        self.bus_number = usb_device.get("bus_number")
        self.address = usb_device.get("address")
        self.identifier = usb_device.get("identifier")


@dataclass
class HardwareInfo:
    versions: MixerVersions
    serial_number: str
    manufactured_date: datetime
    device_type: DeviceType
    usb_device: USBDevice

    def __init__(self, hardware_info: dict):
        self.versions = MixerVersions(hardware_info.get("versions"))
        self.serial_number = hardware_info.get("serial_number")
        self.manufactured_date = datetime.strptime(
            hardware_info.get("manufactured_date"), "%Y-%m-%d"
        )
        self.device_type = hardware_info.get("device_type")
        self.usb_device = USBDevice(hardware_info.get("usb_device"))


# --------------------------------------------------
# Mixer - Fader Status
# --------------------------------------------------


@dataclass
class Scribble:
    file_name: str
    bottom_text: str
    left_text: str
    inverted: bool

    def __init__(self, scribble: dict):
        self.file_name = scribble.get("file_name")
        self.bottom_text = scribble.get("bottom_text")
        self.left_text = scribble.get("left_text")
        self.inverted = scribble.get("inverted")


@dataclass
class FaderStatus:
    channel: Channel
    mute_type: MuteFunction
    scribble: Scribble
    mute_state: MuteState

    def __init__(self, fader_status: dict):
        self.channel = Channel[fader_status.get("channel")]
        self.mute_type = MuteFunction[fader_status.get("mute_type")]
        self.scribble = Scribble(fader_status.get("scribble"))
        self.mute_state = MuteState[fader_status.get("mute_state")]


# --------------------------------------------------
# Mixer - Fader Status
# --------------------------------------------------


@dataclass
class Equaliser:
    gain: Dict[EqFrequency, int]
    frequency: Dict[EqFrequency, float]

    def __init__(self, equaliser: dict):
        self.gain = {EqFrequency[k]: v for k, v in equaliser.get("gain").items()}
        self.frequency = {
            EqFrequency[k]: v for k, v in equaliser.get("frequency").items()
        }


@dataclass
class EqMini(Equaliser):
    gain: Dict[MiniEqFrequency, int]
    frequency: Dict[MiniEqFrequency, float]

    def __init__(self, eq_mini: dict):
        self.gain = {MiniEqFrequency[k]: v for k, v in eq_mini.get("gain").items()}
        self.frequency = {
            MiniEqFrequency[k]: v for k, v in eq_mini.get("frequency").items()
        }


@dataclass
class NoiseGate:
    threshold: int
    attack: int
    release: int
    enabled: bool
    attenuation: int

    def __init__(self, noise_gate: dict):
        self.threshold = noise_gate.get("threshold")
        self.attack = noise_gate.get("attack")
        self.release = noise_gate.get("release")
        self.enabled = noise_gate.get("enabled")
        self.attenuation = noise_gate.get("attenuation")


@dataclass
class Compressor:
    threshold: int
    ratio: int
    attack: int
    release: int
    makeup_gain: int

    def __init__(self, compressor: dict):
        self.threshold = compressor.get("threshold")
        self.ratio = compressor.get("ratio")
        self.attack = compressor.get("attack")
        self.release = compressor.get("release")
        self.makeup_gain = compressor.get("makeup_gain")


@dataclass
class MicStatus:
    mic_type: MicrophoneType
    mic_gains: Dict[MicrophoneType, int]
    equaliser: Equaliser
    equaliser_mini: EqMini
    noise_gate: NoiseGate
    compressor: Compressor

    def __init__(self, mic_status: dict):
        self.mic_type = MicrophoneType[mic_status.get("mic_type")]

        # example: {"Dynamic": 30, "Condenser": 40, "Jack": 30}
        self.mic_gains = {
            MicrophoneType[k]: v for k, v in mic_status.get("mic_gains").items()
        }

        self.equaliser = Equaliser(mic_status.get("equaliser"))
        self.equaliser_mini = EqMini(mic_status.get("equaliser_mini"))

        self.noise_gate = NoiseGate(mic_status.get("noise_gate"))
        self.compressor = Compressor(mic_status.get("compressor"))


# --------------------------------------------------
# Mixer - Levels
# --------------------------------------------------


@dataclass
class Submix:
    volume: int
    linked: bool
    ratio: float

    def __init__(self, submix: dict):
        self.volume = submix.get("volume")
        self.linked = submix.get("linked")
        self.ratio = submix.get("ratio")


@dataclass
class Submixes:
    inputs: Dict[SubMixChannel, Submix]
    outputs: Dict[OutputDevice, Mix]

    def __init__(self, submixes: dict):
        self.inputs = {
            SubMixChannel[k]: Submix(v) for k, v in submixes.get("inputs").items()
        }
        self.outputs = {
            OutputDevice[k]: Mix[v] for k, v in submixes.get("outputs").items()
        }


@dataclass
class Levels:
    submix_supported: bool
    output_monitor: OutputDevice
    volumes: Dict[Channel, int]
    submix: Optional[Submixes]
    bleep: int
    deess: int

    def __init__(self, levels: dict):
        self.submix_supported = levels.get("submix_supported")
        self.output_monitor = OutputDevice[levels.get("output_monitor")]
        self.volumes = {Channel[k]: v for k, v in levels.get("volumes").items()}
        if submix := levels.get("submix"):
            self.submix = {Channel[k]: v for k, v in submix.items()}
        else:
            self.submix = None
        self.bleep = levels.get("bleep")
        self.deess = levels.get("deess")


# --------------------------------------------------
# Mixer - Cough Button
# --------------------------------------------------


@dataclass
class CoughButton:
    is_toggle: bool
    mute_type: MuteFunction
    state: MuteState

    def __init__(self, cough_button: dict):
        self.is_toggle = cough_button.get("is_toggle")
        self.mute_type = MuteFunction[cough_button.get("mute_type")]
        self.mute_state = MuteState[cough_button.get("state")]


# --------------------------------------------------
# Mixer - Lighting
# --------------------------------------------------


@dataclass
class Animation:
    supported: bool
    mode: AnimationMode
    mod1: int
    mod2: int
    waterfall_direction: WaterfallDirection

    def __init__(self, animation: dict):
        self.supported = animation.get("supported")

        # if "None" set to AnimationMode.NONE else AnimationMode[animation.get("mode")]
        # use walrus operator instead of getting the value twice
        self.mode = (
            AnimationMode.NONE
            if (mode := animation.get("mode")) == "None"
            else AnimationMode[mode]
        )

        self.mod1 = animation.get("mod1")
        self.mod2 = animation.get("mod2")
        self.waterfall_direction = WaterfallDirection[
            animation.get("waterfall_direction")
        ]


@dataclass
class Colours:
    """
    Store up to three colours for a lighting style.

    Can be initialised with a dict or up to three strings.
    """

    colour_one: str
    colour_two: Optional[str]
    colour_three: Optional[str]

    def __init__(self, colour1: dict | str, colour2: str = None, colour3: str = None):
        if type(colour1) == str:
            self.colour_one = colour1
            self.colour_two = colour2
            self.colour_three = colour3
        else:
            self.colour_one = colour1.get("colour_one")
            self.colour_two = colour1.get("colour_two")
            self.colour_three = colour1.get("colour_three")


@dataclass
class FaderLighting:
    style: FaderDisplayStyle
    colours: Colours

    def __init__(self, lighting: dict):
        self.style = FaderDisplayStyle[lighting.get("style")]
        self.colours = Colours(lighting.get("colours"))


@dataclass
class ButtonLighting:
    off_style: ButtonColourOffStyle
    colours: Colours

    def __init__(self, lighting: dict):
        self.off_style = ButtonColourOffStyle[lighting.get("off_style")]
        self.colours = Colours(lighting.get("colours"))


@dataclass
class Lighting:
    animation: Animation
    faders: Dict[Fader, FaderLighting]
    buttons: Dict[Button, ButtonLighting]
    simple: Dict[SimpleColourTarget, Colours]
    sampler: Dict[SamplerColourTarget, ButtonLighting]
    encoders: Dict[Encoder, Colours]

    def __init__(self, lighting: dict):
        self.animation = Animation(lighting.get("animation"))
        self.faders = {
            Fader[k]: FaderLighting(v) for k, v in lighting.get("faders").items()
        }
        self.buttons = {
            Button[k]: ButtonLighting(v) for k, v in lighting.get("buttons").items()
        }
        self.simple = {
            SimpleColourTarget[k]: Colours(v) for k, v in lighting.get("simple").items()
        }
        self.sampler = {
            SamplerColourTarget[k]: ButtonLighting(v)
            for k, v in lighting.get("sampler").items()
        }
        self.encoders = {
            Encoder[k]: Colours(v) for k, v in lighting.get("encoders").items()
        }


# --------------------------------------------------
# Mixer - Effects
# --------------------------------------------------


@dataclass
class Reverb:
    style: ReverbStyle
    amount: int
    decay: int
    early_level: int
    tail_level: int
    pre_delay: int
    lo_colour: int
    hi_colour: int
    hi_factor: int
    diffuse: int
    mod_speed: int
    mod_depth: int

    def __init__(self, reverb: dict):
        self.style = ReverbStyle[reverb.get("style")]
        self.amount = reverb.get("amount")
        self.decay = reverb.get("decay")
        self.early_level = reverb.get("early_level")
        self.tail_level = reverb.get("tail_level")
        self.pre_delay = reverb.get("pre_delay")
        self.lo_colour = reverb.get("lo_colour")
        self.hi_colour = reverb.get("hi_colour")
        self.hi_factor = reverb.get("hi_factor")
        self.diffuse = reverb.get("diffuse")
        self.mod_speed = reverb.get("mod_speed")
        self.mod_depth = reverb.get("mod_depth")


@dataclass
class Echo:
    style: EchoStyle
    amount: int
    feedback: int
    tempo: int
    delay_left: int
    delay_right: int
    feedback_left: int
    feedback_right: int
    feedback_xfb_l_to_r: int
    feedback_xfb_r_to_l: int

    def __init__(self, echo: dict):
        self.style = EchoStyle[echo.get("style")]
        self.amount = echo.get("amount")
        self.feedback = echo.get("feedback")
        self.tempo = echo.get("tempo")
        self.delay_left = echo.get("delay_left")
        self.delay_right = echo.get("delay_right")
        self.feedback_left = echo.get("feedback_left")
        self.feedback_right = echo.get("feedback_right")
        self.feedback_xfb_l_to_r = echo.get("feedback_xfb_l_to_r")
        self.feedback_xfb_r_to_l = echo.get("feedback_xfb_r_to_l")


@dataclass
class Pitch:
    style: PitchStyle
    amount: int
    character: int

    def __init__(self, pitch: dict):
        self.style = PitchStyle[pitch.get("style")]
        self.amount = pitch.get("amount")
        self.character = pitch.get("character")


@dataclass
class Gender:
    style: GenderStyle
    amount: int

    def __init__(self, gender: dict):
        self.style = GenderStyle[gender.get("style")]
        self.amount = gender.get("amount")


@dataclass
class Megaphone:
    is_enabled: bool
    style: MegaphoneStyle
    amount: int
    post_gain: int

    def __init__(self, megaphone: dict):
        self.is_enabled = megaphone.get("is_enabled")
        self.style = MegaphoneStyle[megaphone.get("style")]
        self.amount = megaphone.get("amount")
        self.post_gain = megaphone.get("post_gain")


@dataclass
class Robot:
    is_enabled: bool
    style: RobotStyle
    low_gain: int
    low_freq: int
    low_width: int
    mid_gain: int
    mid_freq: int
    mid_width: int
    high_gain: int
    high_freq: int
    high_width: int
    waveform: int
    pulse_width: int
    threshold: int
    dry_mix: int

    def __init__(self, robot: dict):
        self.is_enabled = robot.get("is_enabled")
        self.style = RobotStyle[robot.get("style")]
        self.low_gain = robot.get("low_gain")
        self.low_freq = robot.get("low_freq")
        self.low_width = robot.get("low_width")
        self.mid_gain = robot.get("mid_gain")
        self.mid_freq = robot.get("mid_freq")
        self.mid_width = robot.get("mid_width")
        self.high_gain = robot.get("high_gain")
        self.high_freq = robot.get("high_freq")
        self.high_width = robot.get("high_width")
        self.waveform = robot.get("waveform")
        self.pulse_width = robot.get("pulse_width")
        self.threshold = robot.get("threshold")
        self.dry_mix = robot.get("dry_mix")


@dataclass
class HardTune:
    is_enabled: bool
    style: HardTuneStyle
    amount: int
    rate: int
    window: int
    source: HardTuneSource

    def __init__(self, hard_tune: dict):
        self.is_enabled = hard_tune.get("is_enabled")
        self.style = HardTuneStyle[hard_tune.get("style")]
        self.amount = hard_tune.get("amount")
        self.rate = hard_tune.get("rate")
        self.window = hard_tune.get("window")
        self.source = HardTuneSource[hard_tune.get("source")]


@dataclass
class CurrentEffects:
    reverb: Reverb
    echo: Echo
    pitch: Pitch
    gender: Gender
    megaphone: Megaphone
    robot: Robot
    hard_tune: HardTune

    def __init__(self, effects: dict):
        self.reverb = Reverb(effects.get("reverb"))
        self.echo = Echo(effects.get("echo"))
        self.pitch = Pitch(effects.get("pitch"))
        self.gender = Gender(effects.get("gender"))
        self.megaphone = Megaphone(effects.get("megaphone"))
        self.robot = Robot(effects.get("robot"))
        self.hard_tune = HardTune(effects.get("hard_tune"))


@dataclass
class Effects:
    is_enabled: bool
    active_preset: EffectBankPreset
    preset_names: Dict[EffectBankPreset, str]
    current: CurrentEffects

    def __init__(self, effects: dict):
        self.is_enabled = effects.get("is_enabled")
        self.active_preset = EffectBankPreset[effects.get("active_preset")]
        self.preset_names = effects.get("preset_names")
        self.current = CurrentEffects(effects.get("current"))


# -------------------------------------------------------
# Mixer - Sampler
# -------------------------------------------------------


@dataclass
class Sample:
    name: str
    start_pct: float
    stop_pct: float

    def __init__(self, sample: dict):
        self.name = sample.get("name")
        self.start_pct = sample.get("start_pct")
        self.stop_pct = sample.get("stop_pct")


@dataclass
class SampleMetadata:
    function: SamplePlaybackMode
    order: SamplePlayOrder
    samples: List[Sample]
    is_playing: bool
    is_recording: bool

    def __init__(self, sample_button: dict):
        self.function = SamplePlaybackMode[sample_button.get("function")]
        self.order = SamplePlayOrder[sample_button.get("order")]
        self.samples = [Sample(sample) for sample in sample_button.get("samples")]
        self.is_playing = sample_button.get("is_playing")
        self.is_recording = sample_button.get("is_recording")


@dataclass
class SamplerProcessState:
    progress: Optional[int]
    last_error: Optional[str]

    def __init__(self, process_state: dict):
        self.progress = process_state.get("progress")
        self.last_error = process_state.get("last_error")


@dataclass
class Sampler:
    processing_state: SamplerProcessState
    active_bank: SampleBank
    clear_active: bool
    record_buffer: int
    banks: Dict[SampleBank, Dict[SampleButton, SampleMetadata]]

    def __init__(self, sampler: dict):
        self.processing_state = SamplerProcessState(sampler.get("processing_state"))
        self.active_bank = SampleBank[sampler.get("active_bank")]
        self.clear_active = sampler.get("clear_active")
        self.record_buffer = sampler.get("record_buffer")
        self.banks = sampler.get("banks")


# -------------------------------------------------------
# Mixer - Settings
# -------------------------------------------------------


@dataclass
class DisplaySettings:
    gate: DisplayMode
    compressor: DisplayMode
    equaliser: DisplayMode
    equaliser_fine: DisplayMode

    def __init__(self, display: dict):
        self.gate = DisplayMode[display.get("gate")]
        self.compressor = DisplayMode[display.get("compressor")]
        self.equaliser = DisplayMode[display.get("equaliser")]
        self.equaliser_fine = DisplayMode[display.get("equaliser_fine")]


@dataclass
class MixerSettings:
    display: DisplaySettings
    mute_hold_duration: int
    vc_mute_also_mute_cm: bool

    def __init__(self, settings: dict):
        self.display = DisplaySettings(settings.get("display"))
        self.mute_hold_duration = settings.get("mute_hold_duration")
        self.vc_mute_also_mute_cm = settings.get("vc_mute_also_mute_cm")


# -------------------------------------------------------
# Mixer
# -------------------------------------------------------


@dataclass
class Mixer:
    hardware: HardwareInfo
    shutdown_commands: List[Dict[str, List[str] | str]]
    fader_status: Dict[Fader, FaderStatus]
    mic_status: MicStatus
    levels: Levels
    router: Dict[InputDevice, Dict[OutputDevice, bool]]
    cough_button: CoughButton
    lighting: Lighting
    effects: Effects
    sampler: Sampler
    settings: MixerSettings
    button_down: Dict[Button, bool]
    profile_name: str
    mic_profile_name: str

    def __init__(self, mixer: dict):
        self.hardware = HardwareInfo(mixer.get("hardware"))
        self.shutdown_commands = mixer.get("shutdown_commands")
        self.fader_status = {
            Fader[fader]: FaderStatus(status)
            for fader, status in mixer.get("fader_status").items()
        }
        self.mic_status = MicStatus(mixer.get("mic_status"))
        self.levels = Levels(mixer.get("levels"))
        self.router = {
            InputDevice[k]: {OutputDevice[k]: v for k, v in v.items()}
            for k, v in mixer.get("router").items()
        }
        self.cough_button = CoughButton(mixer.get("cough_button"))
        self.lighting = Lighting(mixer.get("lighting"))
        self.effects = Effects(mixer.get("effects"))
        self.sampler = Sampler(mixer.get("sampler"))
        self.settings = MixerSettings(mixer.get("settings"))
        self.button_down = {
            Button[button]: bool(down)
            for button, down in mixer.get("button_down").items()
        }
        self.profile_name = mixer.get("profile_name")
        self.mic_profile_name = mixer.get("mic_profile_name")


# -------------------------------------------------------
# Paths
# -------------------------------------------------------


@dataclass
class Paths:
    profiles: str
    mic_profiles: str
    samples: str
    presets: str
    icons: str
    logs: str

    def __init__(self, paths: dict):
        self.profiles = paths.get("profile_directory")
        self.mic_profiles = paths.get("mic_profile_directory")
        self.samples = paths.get("samples_directory")
        self.presets = paths.get("presets_directory")
        self.icons = paths.get("icons_directory")
        self.logs = paths.get("logs_directory")


# -------------------------------------------------------
# Files
# -------------------------------------------------------


@dataclass
class Files:
    profiles: List[str]
    mic_profiles: List[str]
    samples: Dict[str, str]
    presets: List[str]
    icons: List[str]

    def __init__(self, files: dict):
        self.profiles = files.get("profiles")
        self.mic_profiles = files.get("mic_profiles")
        self.samples = files.get("samples")
        self.presets = files.get("presets")
        self.icons = files.get("icons")


# -------------------------------------------------------
# Status
# -------------------------------------------------------


@dataclass
class Status:
    config: Config
    mixers: Dict[str, Mixer]
    paths: Paths
    files: Files

    def __init__(self, status: dict):
        self.config = Config(status.get("config"))
        self.mixers = {
            serial: Mixer(mixer) for serial, mixer in status.get("mixers").items()
        }
        self.paths = Paths(status.get("paths"))
        self.files = Files(status.get("files"))
