import bunch
import functools

laser1params = {
  'type':str,
  'product_name':str,
  'emission':bool,
  'health':float,
  'health_txt':str,
  'dl': {
    'legacy':bool,
    'type':str,
    'version':str,
    'model':str,
    'serial_number':str,
    'fru_serial_number':str,
    'ontime':int,
    'ontime_txt':str
  },
  'cc': {
    'path':str,
    'variant':str,
    'enabled':bool,
    'emission':bool,
    'current_set':float,
    'current_offset':float,
    'current_set_dithering':bool,
    'external_input': {
      'signal':int,
      'factor':float,
      'enabled':bool
    },
    'output_filter' : {
      'slew_rate':float,
      'slew_rate_enabled':bool,
      'slew_rate_limited':bool
    },
    'current_act':float,
    'positive_polarity':bool,
    'current_clip':int,
    'current_clip_limit':int,
    'voltage_act':float,
    'voltage_clip':float,
    'feedforward_enabled':bool,
    'feedforward_factor':float,
    'pd':float,
    'aux':float,
    'snubber':bool,
    'status':int,
    'status_txt':str
  },
  'tc': {
    'path':str,
    'enabled':bool,
    'temp_act':float,
    'temp_set':int,
    'external_input': {
      'signal':int,
      'factor':float,
      'enabled':bool
    },
    'ready':bool,
    'fault':bool,
    'status':int,
    'status_txt':str,
    't_loop': {
      'p_gain':float,
      'i_gain':float,
      'd_gain':float,
      'ok_tolerance':float,
      'ok_time':float,
    },
    'limits' : {
      'temp_min':float,
      'temp_max':float,
      'timeout':float, 
      'timed_out': bool,
      'out_of_range': bool
    },
    'current_set':float,
    'current_act':float,
    'temp_set_min':float,
    'temp_set_max':float,
    'temp_roc_enabled':bool,
    'temp_roc_limit':float
  },
  'pc': {
    'path':str,
    'enabled':bool,
    'voltage_set':float,
    'voltage_min':float,
    'voltage_max':float,
    'voltage_set_dithering':bool,
    'external_input': {
      'signal':int,
      'factor':float,
      'enabled':bool
    },
    'output_filter':{
      'slew_rate':float,
      'slew_rate_enabled':bool,
      'slew_rate_limited':bool,
    },
    'voltage_act':float,
    'feedforward_enabled':bool,
    'feedforward_factor':float,
    'heatsink_temp':float,
    'status':float,
    'status_txt': str
  },
  'lock' : {
    'type' : int,
    'lock_without_lockpoint' : bool,
    'state' : int,
    'state_txt' :  str,
    'lock_enabled' : bool,
    'hold' : bool,
    'spectrum_input_channel' : int,
    'pid_selection' : int,
    'setpoint' : float,
    'relock' : {
      'enabled' : bool,
      'output_channel' : int,
      'frequency' : float,
      'amplitude' : float,
      'delay' : float
    },
    'reset': {
      'enabled' : bool,
    },
    'window' : {
      'enabled' : bool,
      'input_channel' : int,
      'level_high' : float,
      'level_low' : float,
      'level_hysteresis' : float
    },
    'pid1' : {
      'enabled' : bool,
      'gain' : {
        'all' : float,
        'p' : float,
        'i' : float,
        'd' : float,
        'i_cutoff' : float,
        'i_cutoff_enabled' : bool,
        'fc_ip' : float,
        'fc_pd' : float
      },
      'sign' : bool,
      'slope' : bool,
      'output_channel' : int,
      'outputlimit' : {
        'enabled' : bool,
        'max' : str
      },
      'hold' : bool,
      'lock_state' : bool,
      'hold_state' : bool,
      'regulating_state' : bool
    },
    'pid2' : {
      'enabled' : bool,
      'gain' : {
        'all' : float,
        'p' : float,
        'i' : float,
        'd' : float,
        'i_cutoff' : float,
        'i_cutoff_enabled' : bool,
        'fc_ip' : float,
        'fc_pd' : float
      },
      'sign' : bool,
      'slope' : bool,
      'output_channel' : int,
      'outputlimit' : {
        'enabled' : bool,
        'max' : str
      },
      'hold' : bool,
      'lock_state' : bool,
      'hold_state' : bool,
      'regulating_state' : bool
    },
    'lockin': {
      'modulation_enabled' : bool,
      'modulation_output_channel' : int,
      'frequency' : float,
      'amplitude' : float,
      'phase_shift' : float,
      'lock_level' : float,
      'auto_lir' : {
        'progress' : float, 
      }
    },
    'lockpoint': {
      'position' : tuple,
      'type' : str,
    },
    'candidate_filter' : {
      'top' : bool,
      'bottom' : bool,
      'positive_edge' : bool,
      'negative_edge' : bool,
      'edge_level' : float,
      'peak_noise_tolerance' : float,
      'edge_min_distance' : float,
    },
    'candidates' :  str,
    'locking_delay' : float,
    'background_trace' :  str,
    'lock_tracking' : tuple,
  },
  'pressure_compensation' : {
    'enabled':bool,
    'air_pressure':float,
    'factor':float,
    'compensation_voltage':float,
  },
  'factory_settings' : {
    'wavelength' : float, 
    'threshold_current' : float, 
    'power' : float, 
    'cc':{
      'feedforward_factor' : float,
      'current_set' : float,
      'current_clip' : float,
      'voltage_clip' : float,
      'positive_polarity' : bool,
      'snubber' : bool,
    },
    'tc' : {
      'temp_min':float,
      'temp_max':float,
      'temp_set':float,
      'temp_roc_enabled':bool,
      'temp_roc_limit':float,
      'current_max':float,
      'current_min':float,
      'p_gain':float,
      'i_gain':float,
      'd_gain':float,
      'c_gain':float,
      'ok_tolerance':float,
      'ok_time':float,
      'timeout':int,
      'power_source':int,
      'ntc_series_resistance':int,
      'ntc_parallel_resistance':int
    },
    'pc': {
      'voltage_min':float,
      'voltage_max':float,
      'feedforward_enabled':bool,
      'feedforward_factor':float,
      'capacitance':float,
      'scan_offset':float,
      'scan_amplitude':float,
      'slew_rate':float,
      'slew_rate_enabled':bool,
      'pressure_compensation_factor':float
    },
  },
  'scan': {
    'enabled':bool,
    'hold':bool,
    'signal_type':int,
    'frequency':float,
    'output_channel':int,
    'unit':str,
    'amplitude':float,
    'offset':float,
    'start':float,
    'end':float
  },
  'wide_scan': {
    'state':int,
    'state_txt':str,
    'output_channel':int,
    'scan_begin':float,
    'scan_end':float,
    'offset':float,
    'amplitude':float,
    'speed':float,
    'duration':float,
    'progress':float,
    'remaining_time':float
  },
  'scope': {
    'variant' : int,
    'update_rate' : float,
    'channel1': {
      'signal' : int,
      'unit' : str,
      'name' : str
    },
    'channel2' : {
      'signal' : int,
      'unit' : str,
      'name' : str
    },
    'channelx': {
      'xy_signal' : int,
      'scope_timescale' : float,
      'spectrum_range' : float,
      'spectrum_omit_dc' : bool,
      'unit' : str,
      'name' : str,
    },
    'timescale' : int,
    'data' : str
  },
  'recorder' : {
    'state' : int,
    'state_txt' :  str,
    'signals' :{
      'channel1' : int,
      'channel2' : int,
      'channelx' : int,
    },
    'recording_time' : float,
    'sample_count_set' : float,
    'sample_count' : float,
    'sampling_interval' : float,
    'data': {
      'channel1': {
        'signal' : int,
        'unit' :  str,
        'name' :  str
      },
      'channel2' : {
        'signal' : int,
        'unit' :  str,
        'name' :  str
      },
      'channelx' : {
        'signal' : int,
        'unit' :  str,
        'name' :  str
      },
      'zoom_data' :  str,
      'zoom_offset' : float,
      'zoom_amplitude' : float,
      'recorded_sample_count' : float,
      'last_valid_sample' : float
    }
  },
  'pd_ext': {
    'input_channel':int,
    'photodiode':int,
    'power':int,
    'cal_offset':float,
    'cal_factor':float
  },
  'power_stabilization': {
    'enabled' : bool,
    'gain': {
      'all' : float,
      'p' : float,
      'i' : float,
      'd' : float
    },
    'sign' : bool,
    'input_channel':int,
    'setpoint':float,
    'window':{
      'enabled' : bool,
      'level_low' : 0,
      'level_hysteresis' : 0
    },
    'hold_output_on_unlock':bool,
    'output_channel':int,
    'input_channel_value_act':int,
    'state':int
  },
  'config' : {
    'source':str,
    'product_name':str,
    'date':str,
    'caption':str,
    'pristine':bool
  }
}

print("class name:")

# recursive = lambda d : [recursive(d[b]) if type(d[b]) == dict else b for b in d ]
# flatten = lambda t : [item for sublist in t for item in sublist if type(sublist) == list]
# composer = lambda d : lambda fn : functools.reduce(lambda f, g: lambda x: f(g(x)), (fn for i in range(d)), lambda x: x)
# getLeaves = lambda depth : lambda dictionary : filter(lambda x : type(x) == str, composer(depth)(flatten)(recursive(dictionary)))

# print(*getLeaves(1)(laser1params),sep='\n')