// Pico Spool Monitor Case - Prototype v1
// Units are millimeters

$fn = 40;

// ----------------------
// Output selector
// ----------------------
//
// Options:
// "base"
// "lid"
// "adapter"
// "preview_base_lid"
// "preview_all"

    output_part = "preview_all";

// ----------------------
// Confirmed hardware
// ----------------------
//
// PCB to case:
// - M2.5x6mm screws
//
// Lid to case:
// - M2.5x6mm screws
//
// Adapter plate to case:
// - M2.5 x 6 mm screws
// - Confirmed: screws do not poke through into enclosure
//
// Adapter plate to 2020/4040 extrusion:
// - M5 screws
// - M5 T-nuts

// ----------------------
// Main dimensions
// ----------------------

pcb_length = 88.9;
pcb_width  = 52.1;

inner_length = 105;
inner_width  = 90;
inner_height = 35;

wall = 3;
floor_thickness = 3;
lid_thickness = 3;

outer_length = inner_length + wall * 2;
outer_width  = inner_width + wall * 2;
outer_height = inner_height + floor_thickness;


// ----------------------
// Logo settings
// ----------------------
logo_file = "KnitSpear Picture1.svg";
// Better later: rename to "knit_spear_logo.svg" and use that.

logo_enabled = true;

// Options: "raised", "engraved", "none"
logo_style = "raised";

// Desired printed logo width on lid
logo_target_width = 250;

// Native SVG viewBox size from:
// viewBox="0 0 547 509"
logo_native_width = 547;
logo_native_height = 509;

logo_depth = 0.8;

// Manual position tuning
logo_offset_x = 0;
logo_offset_y = 75;
logo_scale = logo_target_width / logo_native_width;

// Center logo on lid
logo_center_x = outer_length / 2;
logo_center_y = outer_width / 2;


// ----------------------
// External wall mounting ears
// ----------------------

wall_mount_ears_enabled = true;

ear_length = 16;
ear_width = 18;
ear_thickness = floor_thickness;
ear_hole_diameter = 3.4; // M3 clearance

ear_y = outer_width / 2;

// USB cutout
usb_side = "left";          // currently informational only
usb_cutout_width = 20;      // horizontal opening along Y axis
usb_cutout_height = 11;     // vertical opening along Z axis

usb_center_y = outer_width / 2;
usb_center_z = floor_thickness + 17.5;

// Wire exits
wire_slot_width = 45;
wire_slot_height = 10;
wire_slot_z = floor_thickness + 8;

// Strain relief zip-tie bridges
strain_tab_width = 14;
strain_tab_depth = 5;
strain_tab_height = 4;

strain_slot_width = 9;
strain_slot_depth = 2.5;

strain_relief_z = floor_thickness;

// Rear strain relief location
rear_strain_relief_y = outer_width - wall - 14;

// Front strain relief location
front_strain_relief_y = wall + 9;

// PCB mounting
standoff_height = 5;
standoff_diameter = 6;
standoff_hole_diameter = 2.3; // M2 self-tapping pilot hole

// Board placement inside case
pcb_x = wall + (inner_length - pcb_length) / 2;
pcb_y = wall + (inner_width - pcb_width) / 2;

// Approximate M2 corner hole positions based on board size.
// These are placeholders and may need tuning after test print.
mount_spacing_x = 78.7;
mount_spacing_y = 35.6;

mount_margin_x = (pcb_length - mount_spacing_x) / 2;
mount_margin_y = (pcb_width  - mount_spacing_y) / 2;

mounts = [
    [pcb_x + mount_margin_x,                   pcb_y + mount_margin_y],
    [pcb_x + mount_margin_x + mount_spacing_x, pcb_y + mount_margin_y],
    [pcb_x + mount_margin_x,                   pcb_y + mount_margin_y + mount_spacing_y],
    [pcb_x + mount_margin_x + mount_spacing_x, pcb_y + mount_margin_y + mount_spacing_y]
];


// Lid screw posts - M2.5
lid_post_diameter = 6;
lid_post_hole_diameter = 2.5;
lid_clearance_hole = 2.7;

lid_post_inset = 7.5;
lid_post_height = inner_height;

lid_posts = [
    [lid_post_inset, lid_post_inset],
    [outer_length - lid_post_inset, lid_post_inset],
    [lid_post_inset, outer_width - lid_post_inset],
    [outer_length - lid_post_inset, outer_width - lid_post_inset]
];

// ----------------------
// Bottom accessory mounting holes
// For screw-on adapter plates: 2020/4040 extrusion, brackets, etc.
// ----------------------

accessory_mount_enabled = true;

accessory_hole_diameter = 2.1;   // M2.5 self-tapping pilot
accessory_boss_diameter = 6;
accessory_boss_height = 4;

// Spacing for the adapter mounting pattern
accessory_spacing_x = 70;
accessory_spacing_y = 42;

accessory_center_x = outer_length / 2;
accessory_center_y = outer_width / 2;

accessory_mounts = [
    [accessory_center_x - accessory_spacing_x / 2, accessory_center_y - accessory_spacing_y / 2],
    [accessory_center_x + accessory_spacing_x / 2, accessory_center_y - accessory_spacing_y / 2],
    [accessory_center_x - accessory_spacing_x / 2, accessory_center_y + accessory_spacing_y / 2],
    [accessory_center_x + accessory_spacing_x / 2, accessory_center_y + accessory_spacing_y / 2]
];


// ----------------------
// Utility modules
// ----------------------

module rounded_box(size, radius=3) {
    // Simple rounded rectangle box using hull of cylinders
    hull() {
        translate([radius, radius, 0])
            cylinder(h=size[2], r=radius);

        translate([size[0]-radius, radius, 0])
            cylinder(h=size[2], r=radius);

        translate([radius, size[1]-radius, 0])
            cylinder(h=size[2], r=radius);

        translate([size[0]-radius, size[1]-radius, 0])
            cylinder(h=size[2], r=radius);
    }
}

module standoff(x, y) {
    difference() {
        translate([x, y, floor_thickness])
            cylinder(h=standoff_height, d=standoff_diameter);

        translate([x, y, floor_thickness - 0.2])
            cylinder(h=standoff_height + 0.6, d=standoff_hole_diameter);
    }
}

module lid_post(x, y) {
    difference() {
        translate([x, y, floor_thickness])
            cylinder(h=lid_post_height, d=lid_post_diameter);

        translate([x, y, floor_thickness - 0.2])
            cylinder(h=lid_post_height + 0.6, d=lid_post_hole_diameter);
    }
}

// ----------------------
// rear wire exit / strain relief
// ----------------------
module strain_relief_bridge(x, y) {
    
    difference() {
        // Solid tab block
        translate([
            x - strain_tab_width / 2,
            y,
            strain_relief_z
        ])
            cube([
                strain_tab_width,
                strain_tab_depth,
                strain_tab_height
            ]);

        // Slot through tab for zip tie
        translate([
            x - strain_slot_width / 2,
            y - 0.2,
            strain_relief_z + 1
        ])
            cube([
                strain_slot_width,
                strain_tab_depth + 0.4,
                strain_slot_depth
            ]);
    }
}

// ----------------------
// Base tray
// ----------------------

// ----------------------
// Base tray
// ----------------------

module base_tray() {
    difference() {
        union() {
            // Main hollow base shell
            difference() {
                // Outer shell
                rounded_box([outer_length, outer_width, outer_height], 4);

                // Hollow cavity
                translate([wall, wall, floor_thickness])
                    cube([inner_length, inner_width, inner_height + 1]);

                // USB cutout on left wall
                translate([
                    -1,
                    usb_center_y - usb_cutout_width / 2,
                    usb_center_z - usb_cutout_height / 2
                ])
                    cube([
                        wall + 2,
                        usb_cutout_width,
                        usb_cutout_height
                    ]);

                // Rear cable exit slot
                translate([
                    outer_length / 2 - wire_slot_width / 2,
                    outer_width - wall - 1,
                    wire_slot_z
                ])
                    cube([
                        wire_slot_width,
                        wall + 2,
                        wire_slot_height
                    ]);

                // Front cable exit slot
                translate([
                    outer_length / 2 - wire_slot_width / 2,
                    -1,
                    wire_slot_z
                ])
                    cube([
                        wire_slot_width,
                        wall + 2,
                        wire_slot_height
                    ]);
            }

            // PCB standoffs
            for (m = mounts) {
                standoff(m[0], m[1]);
            }

            // Lid screw posts
            for (p = lid_posts) {
                lid_post(p[0], p[1]);
            }

            // Rear wire strain relief bridges
            strain_relief_bridge(outer_length / 2 - 12, rear_strain_relief_y);
            strain_relief_bridge(outer_length / 2 + 12, rear_strain_relief_y);

            // Front wire strain relief bridges
            strain_relief_bridge(outer_length / 2 - 12, front_strain_relief_y);
            strain_relief_bridge(outer_length / 2 + 12, front_strain_relief_y);

            // Bottom accessory mounting bosses
            if (accessory_mount_enabled) {
                for (a = accessory_mounts) {
                    accessory_mount_boss(a[0], a[1]);
                }
            }

            // External wall mounting ears
            if (wall_mount_ears_enabled) {
                mounting_ear_left();
                mounting_ear_right();
            }
        }

        // Bottom accessory mounting holes
        // These cut through both the base floor and the accessory bosses.
        if (accessory_mount_enabled) {
            for (a = accessory_mounts) {
                translate([a[0], a[1], -0.2])
                    cylinder(
                        h = floor_thickness + accessory_boss_height + 0.8,
                        d = accessory_hole_diameter
                    );
            }
        }
    }
}
// ----------------------
// Lid
// ----------------------
    
module lid() {
    if (logo_style == "raised") {
        union() {
            difference() {
                rounded_box([outer_length, outer_width, lid_thickness], 4);

                // Lid screw clearance holes
                for (p = lid_posts) {
                    translate([p[0], p[1], -0.2])
                        cylinder(
                            h = lid_thickness + 0.4,
                            d = lid_clearance_hole
                        );
                }
            }

            if (logo_enabled) {
                translate([0, 0, lid_thickness])
                    logo_geometry(logo_depth);
            }
        }
    }

    else if (logo_style == "engraved") {
        difference() {
            rounded_box([outer_length, outer_width, lid_thickness], 4);

            // Lid screw clearance holes
            for (p = lid_posts) {
                translate([p[0], p[1], -0.2])
                    cylinder(
                        h = lid_thickness + 0.4,
                        d = lid_clearance_hole
                    );
            }

            if (logo_enabled) {
                translate([0, 0, lid_thickness - logo_depth])
                    logo_geometry(logo_depth + 0.2);
            }
        }
    }

    else {
        difference() {
            rounded_box([outer_length, outer_width, lid_thickness], 4);

            // Lid screw clearance holes
            for (p = lid_posts) {
                translate([p[0], p[1], -0.2])
                    cylinder(
                        h = lid_thickness + 0.4,
                        d = lid_clearance_hole
                    );
            }
        }
    }
}

module logo_geometry(height_value) {
    translate([
        logo_center_x + logo_offset_x,
        logo_center_y + logo_offset_y,
        0
    ])
        scale([logo_scale, logo_scale, 1])
            translate([
                -logo_native_width / 2,
                -logo_native_height / 2,
                0
            ])
                linear_extrude(height = height_value)
                    import(logo_file);
}
    
// ----------------------
// Accessory Mount Boss
// ----------------------
module accessory_mount_boss(x, y) {
    translate([x, y, 0])
        cylinder(
            h = accessory_boss_height,
            d = accessory_boss_diameter
        );
}

// ----------------------
// Mounting Ears
// ----------------------
module mounting_ear_left() {
    difference() {
        hull() {
            // Neck attached to left side of case
            translate([-ear_length / 2, ear_y - ear_width / 2, 0])
                cube([ear_length / 2, ear_width, ear_thickness]);

            // Rounded screw pad outward
            translate([-ear_length, ear_y, 0])
                cylinder(h = ear_thickness, d = ear_width);
        }

        translate([-ear_length, ear_y, -0.2])
            cylinder(
                h = ear_thickness + 0.4,
                d = ear_hole_diameter
            );
    }
}

module mounting_ear_right() {
    difference() {
        hull() {
            // Neck attached to right side of case
            translate([outer_length, ear_y - ear_width / 2, 0])
                cube([ear_length / 2, ear_width, ear_thickness]);

            // Rounded screw pad outward
            translate([outer_length + ear_length, ear_y, 0])
                cylinder(h = ear_thickness, d = ear_width);
        }

        translate([outer_length + ear_length, ear_y, -0.2])
            cylinder(
                h = ear_thickness + 0.4,
                d = ear_hole_diameter
            );
    }
}

// ----------------------
// 2020 / 4040 extrusion adapter plate
// Separate part
// ----------------------

adapter_length = 90;
adapter_width = 50;
adapter_thickness = 5;

adapter_case_hole_diameter = 2.8; // M2.5 clearance
adapter_extrusion_hole_diameter = 5.4; // M5 clearance

// Common 2020/4040 center slot spacing option.
// For a single extrusion rail, one centerline is usually enough.
extrusion_hole_spacing = 40;

module extrusion_adapter_plate() {
    difference() {
        rounded_box([adapter_length, adapter_width, adapter_thickness], 4);

        // Holes that match the case accessory mounting pattern
        for (a = accessory_mounts) {
            translate([
                a[0] - accessory_center_x + adapter_length / 2,
                a[1] - accessory_center_y + adapter_width / 2,
                -0.2
            ])
                cylinder(
                    h = adapter_thickness + 0.4,
                    d = adapter_case_hole_diameter
                );
        }

        // M5 extrusion mounting holes along centerline
        translate([
            adapter_length / 2 - extrusion_hole_spacing / 2,
            adapter_width / 2,
            -0.2
        ])
            cylinder(
                h = adapter_thickness + 0.4,
                d = adapter_extrusion_hole_diameter
            );

        translate([
            adapter_length / 2 + extrusion_hole_spacing / 2,
            adapter_width / 2,
            -0.2
        ])
            cylinder(
                h = adapter_thickness + 0.4,
                d = adapter_extrusion_hole_diameter
            );
    }
}


// ----------------------
// Render selected output
// ----------------------

module render_selected_part() {
    if (output_part == "base") {
        base_tray();
    }

    else if (output_part == "lid") {
        lid();
    }

    else if (output_part == "adapter") {
        extrusion_adapter_plate();
    }

    else if (output_part == "preview_base_lid") {
        base_tray();

        translate([outer_length + ear_length * 2 + 20, 0, 0])
            lid();
    }

    else if (output_part == "preview_all") {
        base_tray();

        translate([outer_length + ear_length * 2 + 20, 0, 0])
            lid();

        translate([0, outer_width + 25, 0])
            extrusion_adapter_plate();
    }

    else {
        echo("Invalid output_part selected.");
        echo("Use: base, lid, adapter, preview_base_lid, or preview_all");
    }
}

render_selected_part();