#############################################################################
# Generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#  Apr 02, 2019 11:25:51 PM EDT  platform: Windows NT
set vTcl(timestamp) ""


if {!$vTcl(borrow)} {

set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) #d9d9d9
set vTcl(analog_color_p) #d9d9d9
set vTcl(analog_color_m) #d9d9d9
set vTcl(active_fg) #000000
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(active_menu_fg) #000000
}

#############################################################################
# vTcl Code to Load User Fonts

vTcl:font:add_font \
    "-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0" \
    user \
    vTcl:font10
vTcl:font:add_font \
    "-family {Segoe UI} -size 9 -weight normal -slant roman -underline 0 -overstrike 0" \
    user \
    vTcl:font9
#################################
#LIBRARY PROCEDURES
#


if {[info exists vTcl(sourcing)]} {

proc vTcl:project:info {} {
    set base .top42
    global vTcl
    set base $vTcl(btop)
    if {$base == ""} {
        set base .top42
    }
    namespace eval ::widgets::$base {
        set dflt,origin 0
        set runvisible 1
    }
    namespace eval ::widgets_bindings {
        set tagslist _TopLevel
    }
    namespace eval ::vTcl::modules::main {
        set procs {
        }
        set compounds {
        }
        set projectType single
    }
}
}

#################################
# GENERATED GUI PROCEDURES
#

proc vTclWindow.top42 {base} {
    if {$base == ""} {
        set base .top42
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background {#ffffff} -highlightbackground {#d9d9d9} \
        -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 600x450+651+212
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 3844 1061
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    wm title $top "Throughput Analysis"
    vTcl:DefineAlias "$top" "Throughput_TL" vTcl:Toplevel:WidgetProc "" 1
    ttk::style configure Label -background #d9d9d9
    ttk::style configure Label -foreground #000000
    ttk::style configure Label -font TkDefaultFont
    label $top.lab43 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font10,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Throughput Analysis} 
    vTcl:DefineAlias "$top.lab43" "Title" vTcl:WidgetProc "Throughput_TL" 1
    button $top.but44 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text Start 
    vTcl:DefineAlias "$top.but44" "StartButton" vTcl:WidgetProc "Throughput_TL" 1
    button $top.but45 \
        -activebackground {#d9d9d9} -activeforeground {#000000} \
        -background {#d9d9d9} -disabledforeground {#a3a3a3} \
        -font TkDefaultFont -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -pady 0 \
        -text Stop 
    vTcl:DefineAlias "$top.but45" "StopButton" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab46 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Valid Packet Ratio} 
    vTcl:DefineAlias "$top.lab46" "vpr_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab47 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Theoretical Throughput} 
    vTcl:DefineAlias "$top.lab47" "tThroughput_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab48 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -text Throughput 
    vTcl:DefineAlias "$top.lab48" "throughput_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab49 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Processing Time} 
    vTcl:DefineAlias "$top.lab49" "processingTime_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab50 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Per Packet Time} 
    vTcl:DefineAlias "$top.lab50" "perPacketTime_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab51 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Theoretical Packet Time} 
    vTcl:DefineAlias "$top.lab51" "tPerPacketTime_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab55 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable vpr_value 
    vTcl:DefineAlias "$top.lab55" "vpr_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab56 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable throughput_value 
    vTcl:DefineAlias "$top.lab56" "throughput_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab57 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable processingTime_value 
    vTcl:DefineAlias "$top.lab57" "processingTime_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab58 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable perPacket_value 
    vTcl:DefineAlias "$top.lab58" "perPacketTime_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab59 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable tThroughput_value 
    vTcl:DefineAlias "$top.lab59" "tThroughput_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab61 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable tPerPacket_value 
    vTcl:DefineAlias "$top.lab61" "tPerPacketTime_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab62 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Valid Packets} 
    vTcl:DefineAlias "$top.lab62" "validPackets_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab63 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Total Packets} 
    vTcl:DefineAlias "$top.lab63" "totalPackets_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab64 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable validPackets_value 
    vTcl:DefineAlias "$top.lab64" "validPackets_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab65 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable totalPackets_value 
    vTcl:DefineAlias "$top.lab65" "totalPackets_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab44 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Message Size} 
    vTcl:DefineAlias "$top.lab44" "msgSize_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab52 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {GUI Update Time} 
    vTcl:DefineAlias "$top.lab52" "guiUpdate_label" vTcl:WidgetProc "Throughput_TL" 1
    entry $top.ent55 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black -justify center \
        -relief groove -selectbackground {#c4c4c4} -selectforeground black \
        -textvariable msgSize_value 
    vTcl:DefineAlias "$top.ent55" "MsgSize_entry" vTcl:WidgetProc "Throughput_TL" 1
    entry $top.ent56 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black -justify center \
        -relief groove -selectbackground {#c4c4c4} -selectforeground black \
        -textvariable guiUpdate_value 
    vTcl:DefineAlias "$top.ent56" "GUIUpdate_Entry" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab42 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black -relief ridge \
        -text ... -textvariable adjustedRXSamples_value 
    vTcl:DefineAlias "$top.lab42" "adjustedRXSamples_value" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab45 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Adjusted RX Samples} 
    vTcl:DefineAlias "$top.lab45" "adjustedRXSamples_label" vTcl:WidgetProc "Throughput_TL" 1
    label $top.lab53 \
        -activebackground {#f9f9f9} -activeforeground black \
        -background {#ffffff} -disabledforeground {#a3a3a3} \
        -font $::vTcl(fonts,vTcl:font9,object) -foreground {#000000} \
        -highlightbackground {#d9d9d9} -highlightcolor black \
        -text {Starting RX Samples} 
    vTcl:DefineAlias "$top.lab53" "startingRXSamples_label" vTcl:WidgetProc "Throughput_TL" 1
    entry $top.ent54 \
        -background white -disabledforeground {#a3a3a3} -font TkFixedFont \
        -foreground {#000000} -highlightbackground {#d9d9d9} \
        -highlightcolor black -insertbackground black -justify center \
        -relief groove -selectbackground {#c4c4c4} -selectforeground black \
        -textvariable startingRXSample_value 
    vTcl:DefineAlias "$top.ent54" "StartingRXSamples_Entry" vTcl:WidgetProc "Throughput_TL" 1
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.lab43 \
        -in $top -x 40 -y 20 -width 174 -relwidth 0 -height 31 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but44 \
        -in $top -x 210 -y 20 -width 77 -relwidth 0 -height 34 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.but45 \
        -in $top -x 300 -y 20 -width 77 -height 34 -anchor nw \
        -bordermode ignore 
    place $top.lab46 \
        -in $top -x 20 -y 160 -width 124 -relwidth 0 -height 31 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab47 \
        -in $top -x 310 -y 240 -width 144 -relwidth 0 -height 31 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab48 \
        -in $top -x 20 -y 200 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab49 \
        -in $top -x 20 -y 240 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab50 \
        -in $top -x 20 -y 280 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab51 \
        -in $top -x 310 -y 280 -width 144 -relwidth 0 -height 31 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab55 \
        -in $top -x 150 -y 160 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab56 \
        -in $top -x 150 -y 200 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab57 \
        -in $top -x 150 -y 240 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab58 \
        -in $top -x 150 -y 280 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab59 \
        -in $top -x 450 -y 240 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab61 \
        -in $top -x 450 -y 280 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab62 \
        -in $top -x 320 -y 160 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab63 \
        -in $top -x 320 -y 200 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab64 \
        -in $top -x 450 -y 160 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab65 \
        -in $top -x 450 -y 200 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab44 \
        -in $top -x 40 -y 70 -width 84 -relwidth 0 -height 31 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab52 \
        -in $top -x 330 -y 70 -width 104 -relwidth 0 -height 31 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.ent55 \
        -in $top -x 150 -y 70 -width 114 -relwidth 0 -height 30 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.ent56 \
        -in $top -x 450 -y 70 -width 114 -relwidth 0 -height 30 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.lab42 \
        -in $top -x 150 -y 320 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab45 \
        -in $top -x 20 -y 320 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.lab53 \
        -in $top -x 20 -y 110 -width 124 -height 31 -anchor nw \
        -bordermode ignore 
    place $top.ent54 \
        -in $top -x 150 -y 110 -width 114 -height 30 -anchor nw \
        -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

#############################################################################
## Binding tag:  _TopLevel

bind "_TopLevel" <<Create>> {
    if {![info exists _topcount]} {set _topcount 0}; incr _topcount
}
bind "_TopLevel" <<DeleteWindow>> {
    if {[set ::%W::_modal]} {
                vTcl:Toplevel:WidgetProc %W endmodal
            } else {
                destroy %W; if {$_topcount == 0} {exit}
            }
}
bind "_TopLevel" <Destroy> {
    if {[winfo toplevel %W] == "%W"} {incr _topcount -1}
}

set btop ""
if {$vTcl(borrow)} {
    set btop .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop $vTcl(tops)] != -1} {
        set btop .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop
Window show .
Window show .top42 $btop
if {$vTcl(borrow)} {
    $btop configure -background plum
}
