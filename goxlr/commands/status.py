from ..error import DaemonError, MixerNotFoundError
from ..types.models import *


class StatusCommands:
    """
    Commands related to getting the status of the GoXLR.
    I decided to split this into its own file because there's
    already enough code in goxlr.py.
    """

    async def get_status(self) -> Status:
        """
        Returns the status of the GoXLR.

        :return: The status of the GoXLR.

        :raises DaemonError: If the status could not be retrieved.

        :note: You should use GoXLR.update() instead of this method.
        """
        status = await self.send("GetStatus")

        if not status:
            raise DaemonError("Failed to get status from daemon.")

        return Status(status)

    # ------------------------------------------------------------
    # Config
    # ------------------------------------------------------------

    def get_http_settings(self) -> HttpSettings:
        """
        :return: The HTTP settings of the GoXLR.
        """
        return self.status.config.http_settings

    def get_daemon_version(self) -> str:
        """
        :return: The version of the GoXLR Utility daemon.
        """
        return self.status.config.daemon_version

    def is_autostart_enabled(self) -> bool:
        """
        :return: Whether or not the GoXLR Utility daemon is set to start on boot.
        """
        return self.status.config.autostart_enabled

    def is_tray_icon_visible(self) -> bool:
        """
        :return: Whether or not the GoXLR Utility daemon is set to show a tray icon.
        """
        return self.status.config.show_tray_icon

    def is_tts_enabled(self) -> bool:
        """
        :return: Whether or not TTS is enabled.
        """
        return self.status.config.tts_enabled

    def is_network_access_allowed(self) -> bool:
        """
        :return: Whether or not network access is allowed.
        """
        return self.status.config.allow_network_access

    def get_log_level(self) -> LogLevel:
        """
        :return: The log level of the GoXLR Utility daemon.
        """
        return self.status.config.log_level

    # ------------------------------------------------------------
    # Mixers
    # ------------------------------------------------------------

    def get_mixer(self, serial: str = None) -> Mixer:
        """
        Returns a mixer object with the specified serial number.

        :param serial: The serial number of the mixer to interact with.
                          If not specified, it will default to the currently selected mixer.

        :return: The requested mixer object.

        :raises MixerNotFoundError: If the specified mixer is not found.
        """
        if not serial:
            return self.mixer  # return the currently selected mixer

        if serial not in self.status.mixers:
            raise MixerNotFoundError(f"Mixer {serial} not found.")

        return self.status.mixers.get(serial)

    # assume that the user wants to interact with the currently selected mixer
    # using self.mixer

    # Hardware Info

    def get_hardware_info(self) -> HardwareInfo:
        return self.mixer.hardware

    def get_versions(self) -> MixerVersions:
        return self.get_hardware_info().versions

    def get_serial_number(self) -> str:
        return self.get_hardware_info().serial_number

    def get_manufactured_date(self) -> datetime:
        return self.get_hardware_info().manufactured_date

    def get_device_type(self) -> DeviceType:
        return self.get_hardware_info().device_type

    def get_usb_device(self) -> USBDevice:
        return self.get_hardware_info().usb_device

    # Shutdown Commands

    def get_shutdown_commands(self) -> List[Dict[str, List[str] | str]]:
        return self.mixer.shutdown_commands

    # Fader Status

    def get_fader_status(self) -> Dict[Fader, FaderStatus]:
        return self.mixer.fader_status

    def get_fader(self, fader: Fader) -> FaderStatus | None:
        return self.get_fader_status().get(fader)

    def get_fader_channel(self, fader: Fader) -> Channel:
        return self.get_fader(fader).channel

    def get_fader_mute_function(self, fader: Fader) -> MuteFunction:
        return self.get_fader(fader).mute_type

    def get_fader_scribble(self, fader: Fader) -> Scribble:
        return self.get_fader(fader).scribble

    def get_fader_scribble_file_name(self, fader: Fader) -> str:
        return self.get_fader_scribble(fader).file_name

    def get_scribble_text(self, fader: Fader) -> str:
        return self.get_fader_scribble(fader).bottom_text

    def get_scribble_left_text(self, fader: Fader) -> str:
        return self.get_fader_scribble(fader).left_text

    def get_scribble_invert(self, fader: Fader) -> bool:
        return self.get_fader_scribble(fader).inverted

    def get_fader_mute_state(self, fader: Fader) -> MuteState:
        return self.get_fader(fader).mute_state

    def is_fader_muted(self, fader: Fader) -> bool:
        """
        Helper method to check if a fader is muted.
        """
        return self.get_fader_mute_state(fader) != MuteState.Unmuted

    # Mic Status

    def get_mic_status(self) -> MicStatus:
        return self.mixer.mic_status

    def get_microphone_type(self) -> MicrophoneType:
        return self.get_mic_status().mic_type

    def get_microphone_gains(self) -> Dict[MicrophoneType, int]:
        return self.get_mic_status().mic_gains

    def get_microphone_gain(self, mic_type: MicrophoneType = None) -> int | None:
        """
        :note: If no mic type is specified, the currently selected mic type will be used.
        """
        if not mic_type:
            mic_type = self.get_mic_type()
        return self.get_mic_gains().get(mic_type)

    def get_eq(self) -> Equaliser:
        return self.get_mic_status().equaliser

    def get_eq_gain(self, frequency: EqFrequency) -> int | None:
        return self.get_eq().gain.get(frequency)

    def get_eq_frequency(self, frequency: EqFrequency) -> float | None:
        return self.get_eq().frequency.get(frequency)

    def get_eq_mini(self) -> EqMini:
        return self.get_mic_status().equaliser_mini

    def get_eq_mini_gain(self, frequency: MiniEqFrequency) -> int | None:
        return self.get_eq_mini().gain.get(frequency)

    def get_eq_mini_frequency(self, frequency: MiniEqFrequency) -> float | None:
        return self.get_eq_mini().frequency.get(frequency)

    def get_noise_gate(self) -> NoiseGate:
        return self.get_mic_status().noise_gate

    def get_compressor(self) -> Compressor:
        return self.get_mic_status().compressor

    # Levels

    def get_levels(self) -> Levels:
        return self.mixer.levels

    def is_submix_supported(self) -> bool:
        return self.get_levels().submix_supported

    def get_monitor_mix(self) -> OutputDevice:
        return self.get_levels().output_monitor

    def get_volumes(self) -> Dict[Channel, int]:
        return self.get_levels().volumes

    def get_volume(self, channel: Channel) -> int | None:
        return self.get_volumes().get(channel)

    def get_submixes(self) -> Submixes | None:
        return self.get_levels().submix

    def get_submix_input_mix(self, channel: SubMixChannel) -> Submix | None:
        return self.get_submixes().inputs.get(channel)

    def get_submix_volume(self, channel: SubMixChannel) -> int | None:
        return self.get_submix_input_mix(channel).volume

    def get_submix_linked(self, channel: SubMixChannel) -> bool | None:
        return self.get_submix_input_mix(channel).linked

    def get_submix_output_mix(self, output: OutputDevice) -> Mix | None:
        return self.get_submixes().outputs.get(output)

    def get_bleep_volume(self) -> int:
        return self.get_levels().bleep

    def get_deesser(self) -> int:
        return self.get_levels().deess

    # Router

    def get_routing_table(self) -> Dict[InputDevice, Dict[OutputDevice, bool]]:
        return self.mixer.router

    def get_routed_outputs(self, input: InputDevice) -> Dict[OutputDevice, bool] | None:
        return self.get_routing_table().get(input)

    def get_router(self, input: InputDevice, output: OutputDevice) -> bool | None:
        # Would rather name this is_routed, but it's to comply with set_router
        return self.get_routed_outputs(input).get(output)

    def get_routed_inputs(self, output: OutputDevice) -> List[InputDevice]:
        inputs = []
        for input, outputs in self.get_routing_table().items():
            if outputs.get(output):
                inputs.append(input)
        return inputs

    # Cough button

    def get_cough_button(self) -> CoughButton:
        return self.mixer.cough_button

    def get_cough_is_hold(self) -> bool:
        return not self.get_cough_button().is_toggle

    def get_cough_mute_function(self) -> MuteFunction:
        return self.get_cough_button().mute_type

    def get_cough_mute_state(self) -> MuteState:
        return self.get_cough_button().mute_state

    def is_cough_button_muted(self) -> bool:
        return self.get_cough_mute_state() != MuteState.Unmuted

    # Lighting

    def get_lighting(self) -> Lighting:
        return self.mixer.lighting

    def get_animation(self) -> Animation:
        return self.get_lighting().animation

    def is_animation_supported(self) -> bool:
        return self.get_animation().supported

    def get_animation_mode(self) -> AnimationMode:
        return self.get_animation().mode

    def get_animation_mod1(self) -> int:
        return self.get_animation().mod1

    def get_animation_mod2(self) -> int:
        return self.get_animation().mod2

    def get_animation_waterfall(self) -> WaterfallDirection:
        return self.get_animation().waterfall_direction

    def get_fader_lighting(self, fader: Fader) -> FaderLighting | None:
        return self.get_lighting().faders.get(fader)

    def get_fader_display_style(self, fader: Fader) -> FaderDisplayStyle | None:
        return self.get_fader_lighting().style

    def get_fader_colours(self, fader: Fader) -> Colours | None:
        return self.get_fader_lighting().colours

    def get_button_lighting(self, button: Button) -> ButtonLighting | None:
        return self.get_lighting().buttons.get(button)

    def get_button_colours(self, button: Button) -> Colours | None:
        return self.get_button_lighting(button).colours

    def get_button_off_style(self, button: Button) -> ButtonColourOffStyle | None:
        return self.get_button_lighting(button).off_style

    def get_simple_colour(self, target: SimpleColourTarget) -> str | None:
        return self.get_lighting().simple.get(target).colour_one

    def get_sample_lighting(self, target: SamplerColourTarget) -> ButtonLighting | None:
        return self.get_lighting().sampler.get(target)

    def get_sample_colours(self, target: SamplerColourTarget) -> Colours | None:
        return self.get_sample_lighting(target).colours

    def get_encoder_colours(self, encoder: Encoder) -> Colours | None:
        return self.get_lighting().encoders.get(encoder).colours

    # Effects

    def get_effects(self) -> Effects:
        return self.mixer.effects

    def is_effects_enabled(self) -> bool:
        return self.get_effects().is_enabled

    def get_active_effect_preset(self) -> EffectBankPreset:
        return self.get_effects().active_preset

    def get_preset_name(self, preset: EffectBankPreset) -> str | None:
        return self.get_effects().preset_names.get(preset)

    def get_current_effects(self) -> CurrentEffects:
        return self.get_effects().current

    def get_reverb(self) -> Reverb:
        return self.get_current_effects().reverb

    def get_reverb_amount(self) -> int:
        return self.get_reverb().amount

    def get_reverb_decay(self) -> int:
        return self.get_reverb().decay

    def get_reverb_diffuse(self) -> int:
        return self.get_reverb().diffuse

    def get_reverb_early_level(self) -> int:
        return self.get_reverb().early_level

    def get_reverb_high_colour(self) -> int:
        return self.get_reverb().hi_colour

    def get_reverb_high_factor(self) -> int:
        return self.get_reverb().hi_factor

    def get_reverb_low_colour(self) -> int:
        return self.get_reverb().lo_colour

    def get_reverb_mod_depth(self) -> int:
        return self.get_reverb().mod_depth

    def get_reverb_mod_speed(self) -> int:
        return self.get_reverb().mod_speed

    def get_reverb_pre_delay(self) -> int:
        return self.get_reverb().pre_delay

    def get_reverb_style(self) -> ReverbStyle:
        return self.get_reverb().style

    def get_reverb_tail_level(self) -> int:
        return self.get_reverb().tail_level

    def get_echo(self) -> Echo:
        return self.get_current_effects().echo

    def get_echo_amount(self) -> int:
        return self.get_echo().amount

    def get_echo_delay_left(self) -> int:
        return self.get_echo().delay_left

    def get_echo_delay_right(self) -> int:
        return self.get_echo().delay_right

    def get_echo_feedback(self) -> int:
        return self.get_echo().feedback

    def get_echo_feedback_left(self) -> int:
        return self.get_echo().feedback_left

    def get_echo_feedback_right(self) -> int:
        return self.get_echo().feedback_right

    def get_echo_feedback_xfb_l_to_r(self) -> int:
        return self.get_echo().feedback_xfb_l_to_r

    def get_echo_feedback_xfb_r_to_l(self) -> int:
        return self.get_echo().feedback_xfb_r_to_l

    def get_echo_style(self) -> EchoStyle:
        return self.get_echo().style

    def get_echo_tempo(self) -> int:
        return self.get_echo().tempo

    def get_pitch(self) -> Pitch:
        return self.get_current_effects().pitch

    def get_pitch_amount(self) -> int:
        return self.get_pitch().amount

    def get_pitch_character(self) -> int:
        return self.get_pitch().character

    def get_pitch_style(self) -> PitchStyle:
        return self.get_pitch().style

    def get_gender(self) -> Gender:
        return self.get_current_effects().gender

    def get_gender_amount(self) -> int:
        return self.get_gender().amount

    def get_gender_style(self) -> GenderStyle:
        return self.get_gender().style

    def get_megaphone(self) -> Megaphone:
        return self.get_current_effects().megaphone

    def get_megaphone_amount(self) -> int:
        return self.get_megaphone().amount

    def is_megaphone_enabled(self) -> bool:
        return self.get_megaphone().is_enabled

    def get_megaphone_post_gain(self) -> int:
        return self.get_megaphone().post_gain

    def get_megaphone_style(self) -> MegaphoneStyle:
        return self.get_megaphone().style

    def get_robot(self) -> Robot:
        return self.get_current_effects().robot

    def get_robot_dry_mix(self) -> int:
        return self.get_robot().dry_mix

    def is_robot_enabled(self) -> bool:
        return self.get_robot().is_enabled

    def get_robot_frequency(self, range: RobotRange) -> int:
        match range:
            case RobotRange.Low:
                return self.get_robot().low_freq
            case RobotRange.Medium:
                return self.get_robot().mid_freq
            case RobotRange.High:
                return self.get_robot().high_freq

    def get_robot_gain(self, range: RobotRange) -> int:
        match range:
            case RobotRange.Low:
                return self.get_robot().low_gain
            case RobotRange.Medium:
                return self.get_robot().mid_gain
            case RobotRange.High:
                return self.get_robot().high_gain

    def get_robot_width(self, range: RobotRange) -> int:
        match range:
            case RobotRange.Low:
                return self.get_robot().low_width
            case RobotRange.Medium:
                return self.get_robot().mid_width
            case RobotRange.High:
                return self.get_robot().high_width

    def get_robot_pulse_width(self) -> int:
        return self.get_robot().pulse_width

    def get_robot_style(self) -> RobotStyle:
        return self.get_robot().style

    def get_robot_threshold(self) -> int:
        return self.get_robot().threshold

    def get_robot_waveform(self) -> int:
        return self.get_robot().waveform

    def get_hardtune(self) -> HardTune:
        return self.get_current_effects().hard_tune

    def is_hardtune_enabled(self) -> bool:
        return self.get_hardtune().is_enabled

    def get_hardtune_amount(self) -> int:
        return self.get_hardtune().amount

    def get_hardtune_rate(self) -> int:
        return self.get_hardtune().rate

    def get_hardtune_source(self) -> HardTuneSource:
        return self.get_hardtune().source

    def get_hardtune_style(self) -> HardTuneStyle:
        return self.get_hardtune().style

    def get_hardtune_window(self) -> int:
        return self.get_hardtune().window

    # Sampler

    def get_sampler(self) -> Sampler:
        return self.mixer.sampler

    def get_sampler_processing_state(self) -> SamplerProcessState:
        return self.get_sampler().processing_state

    def get_sampler_active_bank(self) -> SampleBank:
        return self.get_sampler().active_bank

    def is_clear_sample_process_error(self) -> bool:
        # Not entirely sure what this does?
        return self.get_sampler().clear_active

    def get_sampler_pre_buffer_duration(self) -> int:
        return self.get_sampler().record_buffer

    def get_sample_banks(self) -> Dict[SampleBank, Dict[SampleButton, SampleMetadata]]:
        return self.get_sampler().banks

    def get_sample_bank(
        self, bank: SampleBank
    ) -> Dict[SampleButton, SampleMetadata] | None:
        return self.get_sample_banks().get(bank)

    def get_sample_metadata(
        self, bank: SampleBank, button: SampleButton
    ) -> SampleMetadata | None:
        return self.get_sample_bank(bank).get(button)

    def get_sampler_function(
        self, bank: SampleBank, button: SampleButton
    ) -> SamplePlaybackMode | None:
        return self.get_sample_metadata(bank, button).function

    def get_sampler_order(
        self, bank: SampleBank, button: SampleButton
    ) -> SamplePlayOrder | None:
        return self.get_sample_metadata(bank, button).order

    def get_samples(
        self, bank: SampleBank, button: SampleButton
    ) -> List[Sample] | None:
        return self.get_sample_metadata(bank, button).samples

    def get_sample_start_percent(
        self, bank: SampleBank, button: SampleButton, index: int
    ) -> float | None:
        return self.get_samples(bank, button)[index].start_pct

    def get_sample_stop_percent(
        self, bank: SampleBank, button: SampleButton, index: int
    ) -> float | None:
        return self.get_samples(bank, button)[index].stop_pct

    def get_sample_is_playing(self, bank: SampleBank, button: SampleButton) -> bool:
        return self.get_sample_metadata(bank, button).is_playing

    def get_sample_is_recording(self, bank: SampleBank, button: SampleButton) -> bool:
        return self.get_sample_metadata(bank, button).is_recording

    # Settings

    def get_settings(self) -> MixerSettings:
        return self.mixer.settings

    def get_display(self) -> DisplaySettings:
        return self.get_settings().display

    def get_noise_gate_display_mode(self) -> DisplayMode:
        return self.get_display().gate

    def get_compressor_display_mode(self) -> DisplayMode:
        return self.get_display().compressor

    def get_equaliser_display_mode(self) -> DisplayMode:
        return self.get_display().equaliser

    def get_equaliser_fine_display_mode(self) -> DisplayMode:
        return self.get_display().equaliser_fine

    def get_mute_hold_duration(self) -> int:
        return self.get_settings().mute_hold_duration

    def is_vc_mute_also_mute_cm(self) -> bool:
        return self.get_settings().vc_mute_also_mute_cm

    # Button down

    def get_button_down(self) -> Dict[Button, bool]:
        return self.mixer.button_down

    # Profile name

    def get_profile_name(self) -> str:
        return self.mixer.profile_name

    def get_mic_profile_name(self) -> str:
        return self.mixer.mic_profile_name

    # ------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------

    def get_path(self, path: PathType) -> str:
        """
        Returns the path of the specified path type.

        :param path: The path type to get the path of.

        :return: The path of the specified path type.

        :raises ValueError: If the specified path type is invalid.
        """
        match path:
            case PathType.Profiles:
                return self.status.files.profiles
            case PathType.MicProfiles:
                return self.status.files.mic_profiles
            case PathType.Samples:
                return self.status.files.samples
            case PathType.Presets:
                return self.status.files.presets
            case PathType.Icons:
                return self.status.files.icons
            case PathType.Logs:
                return self.status.files.logs
            case _:
                raise ValueError(f"Invalid path type: {path}")

    # ------------------------------------------------------------
    # Files
    # ------------------------------------------------------------

    def get_files(self, path: PathType) -> list:
        """
        Returns the files of the specified path type.

        :param path: The path type to get the files of.

        :return: The files of the specified path type.

        :raises ValueError: If the specified path type is invalid.
        """
        match path:
            case PathType.Profiles:
                return self.status.files.profiles_files
            case PathType.MicProfiles:
                return self.status.files.mic_profiles
            case PathType.Samples:
                return self.status.files.samples
            case PathType.Presets:
                return self.status.files.presets
            case PathType.Icons:
                return self.status.files.icons
            case _:
                raise ValueError(f"Invalid path type: {path}")
