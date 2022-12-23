def addition(zone_name):
  s = """!###################################
  
    Schedule:Constant ,
      AlwaysOn , !- Name
      On/Off , !- Schedule Type Limits Name
      1.0; !- Hourly Value
  
    OtherEquipment,
      OTHEQ_SENSIBLE, !- Name
      , !- Fuel Use Type
      {zone}, !- Zone or ZoneList or Space or SpaceList Name
      ALWAYSON , !- SCHEDULE Name
      EquipmentLevel , !- Design Level calculation method
      0, !- Design Level {{W}}
      , !- Power per Zone Floor Area {{watts/m2}}
      , !- Power per Person {{watts/person}}
      0, !- Fraction Latent
      , !- Fraction Radiant
      0, !- Fraction Lost
      0, !- Carbon Dioxide Generation Rate
      ; !- End -Use Subcategory
  
    OtherEquipment,
      OTHEQ_LATENT, !- Name
      , !- Fuel Use Type
      {zone}, !- Zone or ZoneList or Space or SpaceList Name
      ALWAYSON , !- SCHEDULE Name
      EquipmentLevel , !- Design Level calculation method
      0, !- Design Level {{W}}
      , !- Power per Zone Floor Area {{watts/m2}}
      , !- Power per Person {{watts/person}}
      1, !- Fraction Latent
      , !- Fraction Radiant
      0, !- Fraction Lost
      0, !- Carbon Dioxide Generation Rate
      ; !- End -Use Subcategory
  
    OtherEquipment,
      OTHEQ_RAD, !- Name
      , !- Fuel Use Type
      {zone}, !- Zone or ZoneList or Space or SpaceList Name
      ALWAYSON , !- SCHEDULE Name
      EquipmentLevel , !- Design Level calculation method
      0, !- Design Level {{W}}
      , !- Power per Zone Floor Area {{watts/m2}}
      , !- Power per Person {{watts/person}}
      , !- Fraction Latent
      1, !- Fraction Radiant
      0, !- Fraction Lost
      0, !- Carbon Dioxide Generation Rate
      ; !- End -Use Subcategory
  
    Output:Variable,{zone},Zone Air Temperature,timestep;
    Output:Variable,{zone},Zone Air Relative Humidity,timestep;
    Output:Variable,Vegetation Temperature,PythonPlugin:OutputVariable,Timestep;
  
    PythonPlugin:Instance,
      CEA_Sim,  !- Name
      Yes,                     !- Run During Warmup Days
      main,  !- Python Module Name
      type205;         !- Plugin Class Name
  
    PythonPlugin:Variables,
      MyGlobals,               !- Name
      VegTemp;     !- Variable Name 1
  
    PythonPlugin:OutputVariable,
      Vegetation Temperature,  !- Name
      VegTemp,     !- Python Plugin Variable Name
      Averaged,                !- Type of Data in Variable
      ZoneTimestep,            !- Update Frequency
      C;                       !- Units"""


  return s.format(zone=zone_name)
