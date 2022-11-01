PRO MLshellrunner
  ;This code is used to check for >= 2 hour windows of clean ASI data after using the Machine Learning 
  ;Python code.
  ;Use as standalone for determinging days with clean 2-hour windows of data (without commented section out on bottom)
  ;OR
  ;Use to initial FFT analysis of data (with commented section on bottom)

  savefilelocation = 'C:\Users\Ken\Desktop\2020Davis\'
  readlocation     = 'G:\2020\'
  Year             = '2020'
  monthsArray = ['April','May','June','July','August','September']
  monthsArray = monthsArray+Year

  print, monthsArray

  dayz=''
  ;Loops through months of interest in data hard-disk
  FOR i =0, N_ELEMENTS(monthsArray)-1 DO BEGIN
    dayz = FILE_SEARCH(readlocation+monthsArray[i]+'\*')
    
    cleandayz =''
    ML_data=[]
    ;Loops through each day of the month on drive
    FOR j =0, FLOOR((N_ELEMENTS(dayz))/3.0)-1 DO BEGIN
      a = STRSPLIT(dayz(j),/EXTRACT,'\')
      datez = a(3)
      ML = FILE_SEARCH(dayz[j]+'\*.csv')
      ML_data = READ_CSV(ML, TYPE="Double", HEADER='')
      ML_dat = ML_data.FIELD1
      
      Clean =fltarr(2)
      CleanSpan =fltarr(2)
      p=0
      ;Checks for threshold value of clean ML (0-1) value.
      FOR k=0, N_ELEMENTS(ML_dat)-1 DO BEGIN
        if ML_dat(k) LE 0.9 THEN BEGIN  ;Current value threshold
          Clean = [[Clean],[k,ML_dat(k)]]
        endif
      ENDFOR
      t=0
      start = Clean(0,0)
      
      ;Loops through each clean frame found before
      FOR k=0, N_ELEMENTS(Clean(0,*))-1 DO BEGIN
        
        IF Clean(0,k)-Clean(0,k-1) LE 18 THEN BEGIN ;Checks for less than 3-min gap in ASI clean data before continuing
          t=t+1
          IF t GT 719 THEN BEGIN  ;Recording 2-hour window of clean data
            CleanSpan = [start,start+t]
            
          ENDIF
        ENDIF ELSE BEGIN
          IF t GT 719 AND CleanSpan(1) NE 0 THEN BEGIN  ;Wites location of data frames for use in spectral analysis
            
            WRITE_CSV,STRCOMPRESS(savefilelocation+datez+'('+STRING(UINT(p))+')'+'.csv',/REMOVE_ALL),start,start+t
            cleandayz=[[cleandayz],[datez+'_'+STRING(UINT(cleanspan(0)))+'-'+STRING(UINT(cleanspan(1)))]]
            print, datez
            print, p
            p=p+1
 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;Comment below here to next semicolon line to check clean windows without FFT analysis
 ;;;;;;;;;;;Produces save location and begins FFT analysis procedure by passing info onto "read_images.pro"
            ;The subtitle is to distinguish between data from the same days.
            dirSubtitle = STRCOMPRESS('_'+STRING(UINT(start))+'-'+STRING(UINT(start+t)))
      
            date =  datez
            path = readlocation + '\' + monthsarray(i) + '\'
            futurePath = STRCOMPRESS(savefilelocation + monthsArray[i] + '\' + datez + dirSubtitle,/REMOVE_ALL)
      
            FILE_MKDIR, futurePath
            print,monthsArray[i]
            
            P = read_images(dateString = date, sourcePath = path, begins = uint(STRING(start)), ends = uint(STRING(start+t)), endDir = STRCOMPRESS(futurePath,/REMOVE_ALL))
            ;Q=M_FFT_AMTM_LOOP(deviationData, locationToSaveTo=endDir)
            debugStop = 1
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;       
          ENDIF
          t=0
          start =clean(0,k)
        ENDELSE
        
        
      ENDFOR
    
  ENDFOR
  ENDFOR
  
END