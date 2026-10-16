from manim import *
import numpy as np


class MassStorageMasterclass(Scene):
    def construct(self):
        self.camera.background_color = "#070b14"

        # Persistent bottom progress bar (tracks 0% -> 100% across the 5-minute video)
        self.setup_progress_bar()

        # Execute all 6 kinetic acts (~302 seconds total runtime)
        self.act_1_architecture_and_objectives()   # ~38s
        self.act_2_magnetic_disk_and_crash()       # ~60s
        self.act_3_io_bus_and_controllers()        # ~44s
        self.act_4_ssd_vs_magnetic_tape()          # ~52s
        self.act_5_mapping_and_clv_cav()           # ~54s
        self.act_6_attachment_nas_san()            # ~54s

    # =========================================================================
    # UI INFRASTRUCTURE: Persistent Progress Bar & Section Banners
    # =========================================================================
    def setup_progress_bar(self):
        self.prog_bg = Line(LEFT * 6.5, RIGHT * 6.5, color=GREY_E, stroke_width=6).to_edge(DOWN, buff=0.18)
        self.prog_fill = Line(LEFT * 6.5, LEFT * 6.49, color=TEAL_B, stroke_width=6).to_edge(DOWN, buff=0.18)
        self.prog_lbl = Text("CH 10: MASS-STORAGE STRUCTURE", font_size=12, color=GREY_B).next_to(
            self.prog_bg, UP, buff=0.06, aligned_edge=LEFT
        )
        self.add(self.prog_bg, self.prog_fill, self.prog_lbl)

    def advance_progress(self, fraction, label_text):
        target_end = LEFT * 6.5 + RIGHT * (13.0 * fraction)
        new_line = Line(LEFT * 6.5, target_end, color=TEAL_B, stroke_width=6).to_edge(DOWN, buff=0.18)
        new_lbl = Text(label_text, font_size=12, color=TEAL_A).next_to(
            self.prog_bg, UP, buff=0.06, aligned_edge=LEFT
        )
        return AnimationGroup(Transform(self.prog_fill, new_line), Transform(self.prog_lbl, new_lbl))

    def build_banner(self, section_code, title_text, subtitle_text):
        badge = RoundedRectangle(
            width=1.4, height=0.42, corner_radius=0.08, color=BLUE_C, fill_color=BLUE_E, fill_opacity=0.9
        )
        badge_txt = Text(section_code, font_size=16, color=WHITE, weight=BOLD).move_to(badge.get_center())
        badge_grp = VGroup(badge, badge_txt)

        title = Text(title_text, font_size=26, color=WHITE, weight=BOLD)
        top_row = VGroup(badge_grp, title).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.25).to_edge(LEFT, buff=0.5)

        sub = Text(subtitle_text, font_size=16, color=GREY_B).next_to(top_row, DOWN, buff=0.1, aligned_edge=LEFT)
        sep = Line(LEFT * 6.5, RIGHT * 6.5, color=GREY_D, stroke_width=1.5).next_to(sub, DOWN, buff=0.12)
        sep.set_x(0)
        return VGroup(top_row, sub, sep)

    def clear_stage(self):
        keep = {self.prog_bg, self.prog_fill, self.prog_lbl}
        to_remove = [m for m in self.mobjects if m not in keep]
        for m in to_remove:
            m.clear_updaters()
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove], run_time=0.8)

    # =========================================================================
    # ACT 1: File System 3-Part Architecture & Objectives (~38s)
    # =========================================================================
    def act_1_architecture_and_objectives(self):
        self.play(
            self.advance_progress(0.08, "ACT 1/6: FILE SYSTEM HIERARCHY & CHAPTER 10 OBJECTIVES"),
            run_time=0.8
        )

        # Title Intro
        ch_tag = Text("OPERATING SYSTEM CONCEPTS • CHAPTER 10", font_size=18, color=TEAL_B, weight=BOLD)
        main_title = Text("Mass-Storage Structure", font_size=48, color=WHITE, weight=BOLD).next_to(ch_tag, DOWN, buff=0.2)
        sub_title = Text(
            "Physical Secondary Storage, Performance Metrics, Disk Addressing & Attachment Topologies",
            font_size=18, color=GREY_B
        ).next_to(main_title, DOWN, buff=0.2)
        intro_grp = VGroup(ch_tag, main_title, sub_title).move_to(UP * 1.8)

        self.play(FadeIn(ch_tag, shift=DOWN * 0.2), Write(main_title), FadeIn(sub_title), run_time=2.5)
        self.wait(1.5)

        # 3-Layer File System Logical Stack (Left Side)
        stack_title = Text("3-Part Logical File System", font_size=20, color=BLUE_B, weight=BOLD).move_to(LEFT * 3.4 + UP * 0.3)

        def make_layer(lbl, sub_lbl, col, is_active=False):
            rect = RoundedRectangle(
                width=5.2, height=0.85, corner_radius=0.12,
                color=col, fill_color=col, fill_opacity=0.28 if is_active else 0.12,
                stroke_width=3 if is_active else 1.5
            )
            t1 = Text(lbl, font_size=17, color=WHITE, weight=BOLD)
            t2 = Text(sub_lbl, font_size=14, color=GREY_A)
            txt = VGroup(t1, t2).arrange(DOWN, buff=0.06).move_to(rect.get_center())
            return VGroup(rect, txt)

        layer_ch11 = make_layer("Chapter 11: User & Programmer Interface", "File manipulation, directory trees, access APIs", BLUE_D)
        layer_ch12 = make_layer("Chapter 12: Internal Data Structures & Algorithms", "OS implementation, allocation & free-space management", TEAL_D)
        layer_ch10 = make_layer("Chapter 10: Lowest Level — Secondary Storage", "Magnetic disks, SSDs, tapes, scheduling, formatting & RAID", YELLOW_C, is_active=True)

        layers = VGroup(layer_ch11, layer_ch12, layer_ch10).arrange(DOWN, buff=0.22).next_to(stack_title, DOWN, buff=0.25)
        arrows_down = VGroup(
            Arrow(layer_ch11.get_bottom(), layer_ch12.get_top(), buff=0.04, color=GREY_B, stroke_width=2),
            Arrow(layer_ch12.get_bottom(), layer_ch10.get_top(), buff=0.04, color=YELLOW_B, stroke_width=2),
        )

        self.play(
            intro_grp.animate.scale(0.65).to_edge(UP, buff=0.25),
            Write(stack_title),
            run_time=1.5
        )
        self.play(
            FadeIn(layer_ch11, shift=DOWN * 0.2),
            GrowArrow(arrows_down[0]),
            FadeIn(layer_ch12, shift=DOWN * 0.2),
            GrowArrow(arrows_down[1]),
            FadeIn(layer_ch10, shift=DOWN * 0.2),
            run_time=3.0
        )
        self.play(Indicate(layer_ch10, color=YELLOW, scale_factor=1.04), run_time=1.5)

        # Chapter Objectives Panel (Right Side)
        obj_panel = RoundedRectangle(
            width=6.0, height=3.3, corner_radius=0.15, color=TEAL_C, fill_color="#0f172a", fill_opacity=0.9
        ).move_to(RIGHT * 3.1 + DOWN * 1.1)
        obj_hdr = Text("Core Chapter 10 Objectives", font_size=20, color=TEAL_B, weight=BOLD).next_to(
            obj_panel.get_top(), DOWN, buff=0.22
        )

        obj_items = VGroup(
            Text("1. Physical structure of secondary & tertiary storage", font_size=15, color=WHITE),
            Text("2. Performance metrics: Transfer rate, Seek & Latency", font_size=15, color=WHITE),
            Text("3. Logical Block Addressing (LBA), CLV & CAV zones", font_size=15, color=WHITE),
            Text("4. Host-Attached, NAS & SAN storage architectures", font_size=15, color=WHITE),
            Text("5. Disk scheduling, boot/bad blocks, swap & RAID", font_size=15, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(obj_hdr, DOWN, buff=0.25)

        self.play(FadeIn(obj_panel), Write(obj_hdr), run_time=1.5)
        for item in obj_items:
            self.play(FadeIn(item, shift=RIGHT * 0.25), run_time=1.2)
            self.wait(1.8)

        # Animated I/O request pulse traveling down the 3-layer stack
        io_dot = Dot(color=YELLOW, radius=0.1).move_to(layer_ch11.get_left() + RIGHT * 0.3)
        io_lbl = Text("I/O Request", font_size=13, color=YELLOW).next_to(io_dot, LEFT, buff=0.1)
        io_pulse = VGroup(io_dot, io_lbl)
        self.play(FadeIn(io_pulse), run_time=0.6)
        self.play(io_pulse.animate.move_to(layer_ch12.get_left() + RIGHT * 0.3 + LEFT * 0.45), run_time=1.8)
        self.play(io_pulse.animate.move_to(layer_ch10.get_left() + RIGHT * 0.3 + LEFT * 0.45), run_time=1.8)
        self.play(Flash(io_dot, color=YELLOW, flash_radius=0.35), run_time=1.0)
        self.wait(4.5)

        self.clear_stage()

    # =========================================================================
    # ACT 2: Magnetic Disks (Fig 10.1), RPM/Seek/Latency & Head Crash (~60s)
    # =========================================================================
    def act_2_magnetic_disk_and_crash(self):
        self.play(
            self.advance_progress(0.28, "ACT 2/6: 10.1.1 MAGNETIC DISKS, KINEMATICS & HEAD CRASH"),
            run_time=0.8
        )
        banner = self.build_banner(
            "10.1.1", "Magnetic Disks & Moving-Head Mechanism",
            "1.8\"–3.5\" Platters • Concentric Cylinders • 5,400–15,000 RPM • Micron Air Cushion"
        )
        self.play(FadeIn(banner), run_time=1.2)

        # --- PART 2A: 2.5D Isometric Multi-Platter Stack (Figure 10.1) ---
        stack_x = -3.6
        y_levels = [0.9, -0.3, -1.5]
        spindle_back = Line([stack_x, 1.6, 0], [stack_x, -2.2, 0], color=GREY_B, stroke_width=8)

        platters_25d = VGroup()
        tracks_25d = VGroup()
        for y in y_levels:
            p = Ellipse(width=3.8, height=1.15, color=GREY_B, fill_color="#1e293b", fill_opacity=0.92, stroke_width=2.5)
            p.move_to([stack_x, y, 0])
            t_outer = Ellipse(width=2.5, height=0.75, color=TEAL_C, stroke_width=2.0).move_to([stack_x, y, 0])
            t_inner = Ellipse(width=1.9, height=0.57, color=TEAL_D, stroke_width=1.5).move_to([stack_x, y, 0])
            hub = Ellipse(width=0.45, height=0.15, color=WHITE, fill_color=GREY_A, fill_opacity=1.0).move_to([stack_x, y, 0])
            platters_25d.add(VGroup(p, hub))
            tracks_25d.add(VGroup(t_outer, t_inner))

        # Dashed vertical lines illustrating Cylinder c across all platters
        cyl_left = DashedLine([stack_x - 1.25, y_levels[0], 0], [stack_x - 1.25, y_levels[2], 0], color=YELLOW_B, stroke_width=2)
        cyl_right = DashedLine([stack_x + 1.25, y_levels[0], 0], [stack_x + 1.25, y_levels[2], 0], color=YELLOW_B, stroke_width=2)
        cyl_lbl = Text("Cylinder c\n(Same track on\nall platters)", font_size=13, color=YELLOW_B).move_to([stack_x - 2.35, -0.3, 0])

        # Comb Arm Assembly on right of stack
        post_25d = Rectangle(width=0.38, height=3.2, color=GREY_A, fill_color=GREY_D, fill_opacity=1.0).move_to([stack_x + 2.55, -0.3, 0])
        post_lbl = Text("Arm\nAssembly", font_size=13, color=GREY_A).next_to(post_25d, DOWN, buff=0.12)
        arms_25d = VGroup()
        for y in y_levels:
            arm = Line([stack_x + 2.36, y + 0.14, 0], [stack_x + 1.1, y + 0.14, 0], color=GREY_A, stroke_width=5)
            head = Rectangle(width=0.22, height=0.1, color=RED_B, fill_color=RED, fill_opacity=1.0).move_to([stack_x + 1.05, y + 0.14, 0])
            arms_25d.add(VGroup(arm, head))

        fig10_1_lbl = Text("Figure 10.1: Moving-Head Disk Mechanism", font_size=15, color=BLUE_B, weight=BOLD).move_to([stack_x, -2.55, 0])

        self.play(Create(spindle_back), FadeIn(platters_25d), Create(tracks_25d), run_time=2.5)
        self.play(Create(cyl_left), Create(cyl_right), FadeIn(cyl_lbl), FadeIn(post_25d), FadeIn(post_lbl), FadeIn(arms_25d), Write(fig10_1_lbl), run_time=2.5)

        # Animate unified comb arm movement in 2.5D
        self.play(arms_25d.animate.shift(LEFT * 0.35), run_time=1.8)
        self.play(arms_25d.animate.shift(RIGHT * 0.35), run_time=1.8)

        # --- PART 2B: Top-Down Kinematic Disk & Live Telemetry Dashboard ---
        top_center = RIGHT * 0.8 + DOWN * 0.2
        top_platter = Circle(radius=1.85, color=GREY_B, fill_color="#162032", fill_opacity=1.0, stroke_width=2.5).move_to(top_center)
        top_tracks = VGroup(*[
            Circle(radius=r, color=BLUE_E, stroke_width=1.3).move_to(top_center)
            for r in [0.65, 1.05, 1.45, 1.75]
        ])

        num_sec = 12
        da = TAU / num_sec
        sec_ring = VGroup()
        for i in range(num_sec):
            is_tgt = (i == 5)
            wedge = AnnularSector(
                inner_radius=1.05, outer_radius=1.45, angle=da, start_angle=i * da,
                fill_color=YELLOW if is_tgt else TEAL_E,
                fill_opacity=0.9 if is_tgt else 0.45,
                stroke_color=WHITE, stroke_width=1.0
            ).shift(top_center)
            sec_ring.add(wedge)

        top_spindle = Circle(radius=0.22, color=WHITE, fill_color=GREY_A, fill_opacity=1.0).move_to(top_center)
        spinning_top_disk = VGroup(top_platter, top_tracks, sec_ring, top_spindle)

        top_head = Rectangle(width=0.24, height=0.16, color=RED_A, fill_color=RED, fill_opacity=1.0).move_to(top_center + RIGHT * 1.6)
        top_pivot = Dot(top_center + RIGHT * 2.35 + DOWN * 0.9, color=GREY_A, radius=0.1)
        top_arm_line = always_redraw(lambda: Line(top_pivot.get_center(), top_head.get_center(), color=GREY_A, stroke_width=6))

        # Telemetry Panel on Far Right
        tele_box = RoundedRectangle(width=3.3, height=3.8, corner_radius=0.12, color=BLUE_D, fill_color="#0f172a", fill_opacity=0.95).move_to(RIGHT * 4.85 + DOWN * 0.2)
        tele_hdr = Text("LIVE DISK TELEMETRY", font_size=15, color=TEAL_B, weight=BOLD).next_to(tele_box.get_top(), DOWN, buff=0.18)

        rpm_val = ValueTracker(5400)
        seek_val = ValueTracker(0.0)
        lat_val = ValueTracker(0.0)
        xfer_val = ValueTracker(0.0)

        rpm_lbl = Text("Spindle Speed (RPM):", font_size=13, color=GREY_B).move_to(tele_box.get_top() + DOWN * 0.65 + LEFT * 0.45)
        rpm_num = always_redraw(lambda: Text(f"{int(rpm_val.get_value()):,} RPM", font_size=18, color=GREEN_B, weight=BOLD).next_to(rpm_lbl, DOWN, buff=0.06, aligned_edge=LEFT))

        seek_lbl = Text("1. Seek Time (Arm -> Cyl):", font_size=13, color=GREY_B).next_to(rpm_lbl, DOWN, buff=0.52, aligned_edge=LEFT)
        seek_num = always_redraw(lambda: Text(f"{seek_val.get_value():.1f} ms", font_size=17, color=YELLOW_B, weight=BOLD).next_to(seek_lbl, DOWN, buff=0.06, aligned_edge=LEFT))

        lat_lbl = Text("2. Rotational Latency:", font_size=13, color=GREY_B).next_to(seek_lbl, DOWN, buff=0.52, aligned_edge=LEFT)
        lat_num = always_redraw(lambda: Text(f"{lat_val.get_value():.1f} ms", font_size=17, color=ORANGE, weight=BOLD).next_to(lat_lbl, DOWN, buff=0.06, aligned_edge=LEFT))

        xfer_lbl = Text("3. Transfer Rate:", font_size=13, color=GREY_B).next_to(lat_lbl, DOWN, buff=0.52, aligned_edge=LEFT)
        xfer_num = always_redraw(lambda: Text(f"{xfer_val.get_value():.0f} MB/s", font_size=17, color=TEAL_A, weight=BOLD).next_to(xfer_lbl, DOWN, buff=0.06, aligned_edge=LEFT))

        self.play(
            FadeIn(spinning_top_disk), FadeIn(top_pivot), FadeIn(top_arm_line), FadeIn(top_head),
            FadeIn(tele_box), Write(tele_hdr),
            FadeIn(rpm_lbl), FadeIn(rpm_num), FadeIn(seek_lbl), FadeIn(seek_num),
            FadeIn(lat_lbl), FadeIn(lat_num), FadeIn(xfer_lbl), FadeIn(xfer_num),
            run_time=2.5
        )

        # Step 1: Ramp RPM (5,400 -> 7,200 -> 10,000 -> 15,000 RPM) while spinning platter
        self.play(
            Rotate(spinning_top_disk, angle=TAU * 1.5, about_point=top_center, rate_func=linear),
            rpm_val.animate.set_value(7200),
            run_time=3.5
        )
        self.play(
            Rotate(spinning_top_disk, angle=TAU * 2.0, about_point=top_center, rate_func=linear),
            rpm_val.animate.set_value(15000),
            run_time=3.5
        )

        # Step 2: Seek Time (Move head radially onto target track r=1.25)
        self.play(
            top_head.animate.move_to(top_center + RIGHT * 1.25),
            seek_val.animate.set_value(4.2),
            Rotate(spinning_top_disk, angle=PI, about_point=top_center, rate_func=linear),
            run_time=3.5
        )

        # Step 3: Rotational Latency (Spin yellow target sector 5 under the head at angle 0)
        align_angle = -(5.5 * da) - PI + TAU
        self.play(
            Rotate(spinning_top_disk, angle=align_angle, about_point=top_center, rate_func=smooth),
            lat_val.animate.set_value(2.0),
            run_time=3.5
        )
        self.play(
            Indicate(top_head, color=YELLOW, scale_factor=1.3),
            xfer_val.animate.set_value(145),
            run_time=2.0
        )
        self.wait(2.0)

        # --- PART 2C: Microscopic Air Cushion & Head Crash Simulation ---
        crash_box = RoundedRectangle(
            width=12.6, height=1.55, corner_radius=0.12, color=RED_C, fill_color="#1a0c12", fill_opacity=0.96
        ).move_to(DOWN * 2.55)
        crash_title = Text("MICROSCOPIC VIEW: Head Crash Risk & Removable Media", font_size=15, color=RED_B, weight=BOLD).next_to(
            crash_box.get_top(), DOWN, buff=0.12, aligned_edge=LEFT
        ).shift(RIGHT * 0.25)

        platter_surf = Line(LEFT * 5.8 + DOWN * 3.1, LEFT * 0.5 + DOWN * 3.1, color=TEAL_C, stroke_width=8)
        prot_layer = Line(LEFT * 5.8 + DOWN * 3.02, LEFT * 0.5 + DOWN * 3.02, color=YELLOW_D, stroke_width=2)
        slider_block = Polygon(
            [-4.2, -2.55, 0], [-3.1, -2.55, 0], [-3.2, -2.85, 0], [-4.3, -2.8, 0],
            color=RED_B, fill_color=GREY_B, fill_opacity=0.9
        )
        air_arrows = VGroup(*[
            Arrow([x, -2.93, 0], [x + 0.5, -2.93, 0], buff=0, stroke_width=2, color=BLUE_A)
            for x in [-5.4, -4.6, -3.8, -3.0]
        ])
        air_txt = Text(
            "• Read-write head flies on a micron-thin cushion of air.\n"
            "• Head Crash: Head contacts & gouges magnetic surface -> Entire disk must be replaced!\n"
            "• Removable Disks: Single platter in plastic case, CD/DVD/Blu-ray, or Flash Drives (SSD).",
            font_size=13, color=WHITE, line_spacing=1.25
        ).move_to(RIGHT * 2.85 + DOWN * 2.65)

        self.play(FadeIn(crash_box), Write(crash_title), Create(platter_surf), Create(prot_layer), FadeIn(slider_block), FadeIn(air_arrows), FadeIn(air_txt), run_time=2.5)

        # Animate normal flying then catastrophic head crash contact!
        self.play(slider_block.animate.shift(RIGHT * 1.2), run_time=2.5)
        self.play(slider_block.animate.shift(RIGHT * 0.8 + DOWN * 0.2), run_time=1.2)
        sparks = Flash(slider_block.get_bottom(), color=RED, flash_radius=0.45, num_lines=12)
        damage_scar = Line(LEFT * 2.4 + DOWN * 3.05, LEFT * 1.2 + DOWN * 3.05, color=RED, stroke_width=6)
        self.play(sparks, slider_block.animate.shift(RIGHT * 1.0), Create(damage_scar), run_time=2.0)
        self.wait(4.5)

        self.clear_stage()

    # =========================================================================
    # ACT 3: I/O Buses, Controllers, Cache & Transfer Rates (~44s)
    # =========================================================================
    def act_3_io_bus_and_controllers(self):
        self.play(
            self.advance_progress(0.45, "ACT 3/6: I/O BUSES, CONTROLLERS, CACHE & EFFECTIVE TRANSFER RATES"),
            run_time=0.8
        )
        banner = self.build_banner(
            "10.1.1", "I/O Bus Protocols, Controllers & Built-In Disk Cache",
            "Memory-Mapped I/O Ports • Host Controller vs. Disk Controller • Stated vs. Effective Transfer Rate"
        )
        self.play(FadeIn(banner), run_time=1.2)

        # Architecture Pipeline: CPU/Memory -> Host Controller -> I/O Bus -> Disk Controller (Cache) -> Platter
        cpu_box = RoundedRectangle(width=2.3, height=2.2, corner_radius=0.12, color=GREEN_C, fill_color="#0f291e", fill_opacity=0.9).move_to(LEFT * 5.0 + UP * 0.2)
        cpu_lbl = Text("Computer Host", font_size=16, color=GREEN_B, weight=BOLD).next_to(cpu_box.get_top(), DOWN, buff=0.15)
        mmio_box = RoundedRectangle(width=1.9, height=0.55, corner_radius=0.06, color=GREEN_A, fill_opacity=0.2).move_to(cpu_box.get_center() + UP * 0.25)
        mmio_txt = Text("Memory-Mapped\nI/O Ports", font_size=12, color=WHITE).move_to(mmio_box)
        host_ctrl = RoundedRectangle(width=1.9, height=0.65, corner_radius=0.06, color=TEAL_B, fill_color=TEAL_E, fill_opacity=0.8).move_to(cpu_box.get_center() + DOWN * 0.5)
        host_ctrl_txt = Text("Host Controller", font_size=13, color=WHITE, weight=BOLD).move_to(host_ctrl)

        # Bus Wires in Center
        bus_top = Line(LEFT * 3.85 + UP * 0.4, LEFT * 0.45 + UP * 0.4, color=YELLOW_C, stroke_width=4)
        bus_bot = Line(LEFT * 3.85 + DOWN * 0.2, LEFT * 0.45 + DOWN * 0.2, color=YELLOW_C, stroke_width=4)
        bus_title = Text("I/O Bus Wires", font_size=15, color=YELLOW_B, weight=BOLD).move_to(LEFT * 2.15 + UP * 0.75)
        bus_types = Text("ATA • SATA • eSATA\nUSB • Fibre Channel (FC)", font_size=12, color=GREY_A).move_to(LEFT * 2.15 + DOWN * 0.65)
        fast_lbl = Text("Fast Electronic Speeds", font_size=12, color=GREEN_B).move_to(LEFT * 2.15 + UP * 0.1)

        # Disk Drive Unit on Right
        drive_box = RoundedRectangle(width=6.4, height=2.6, corner_radius=0.14, color=BLUE_C, fill_color="#111c2d", fill_opacity=0.92).move_to(RIGHT * 2.8 + UP * 0.2)
        drive_lbl = Text("Disk Drive Hardware", font_size=16, color=BLUE_B, weight=BOLD).next_to(drive_box.get_top(), DOWN, buff=0.15)

        disk_ctrl = RoundedRectangle(width=2.5, height=1.7, corner_radius=0.1, color=PURPLE_B, fill_color="#23153c", fill_opacity=0.9).move_to(RIGHT * 1.05 + UP * 0.05)
        dc_title = Text("Disk Controller", font_size=14, color=PURPLE_A, weight=BOLD).next_to(disk_ctrl.get_top(), DOWN, buff=0.12)
        cache_slots = VGroup(*[
            Square(side_length=0.32, color=YELLOW_B, fill_color=YELLOW_E, fill_opacity=0.35)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.06).move_to(disk_ctrl.get_center() + DOWN * 0.2)
        cache_lbl = Text("Built-In SRAM Cache", font_size=12, color=YELLOW_B).next_to(cache_slots, UP, buff=0.08)

        mini_platter = VGroup(
            Circle(radius=0.85, color=GREY_B, fill_color="#1e293b", fill_opacity=1.0),
            Circle(radius=0.55, color=TEAL_D, stroke_width=1.5),
            Circle(radius=0.15, color=WHITE, fill_color=GREY_A, fill_opacity=1.0),
            Line(ORIGIN, RIGHT * 0.75, color=RED_B, stroke_width=4)
        ).move_to(RIGHT * 4.65 + UP * 0.05)
        mech_arrow = DoubleArrow(disk_ctrl.get_right(), mini_platter.get_left(), buff=0.08, color=ORANGE, stroke_width=3)
        mech_lbl = Text("Mechanical\nSpeed", font_size=11, color=ORANGE).next_to(mech_arrow, UP, buff=0.05)

        self.play(
            FadeIn(cpu_box), Write(cpu_lbl), FadeIn(mmio_box, mmio_txt), FadeIn(host_ctrl, host_ctrl_txt),
            Create(bus_top), Create(bus_bot), Write(bus_title), FadeIn(bus_types), FadeIn(fast_lbl),
            FadeIn(drive_box), Write(drive_lbl), FadeIn(disk_ctrl), Write(dc_title), FadeIn(cache_lbl), Create(cache_slots),
            FadeIn(mini_platter), GrowArrow(mech_arrow), FadeIn(mech_lbl),
            run_time=3.5
        )

        # Animate Step-by-Step I/O Operation
        cmd_pkt = RoundedRectangle(width=0.75, height=0.3, corner_radius=0.05, color=YELLOW, fill_color=YELLOW, fill_opacity=0.9)
        cmd_txt = Text("CMD", font_size=11, color=BLACK, weight=BOLD).move_to(cmd_pkt)
        pkt = VGroup(cmd_pkt, cmd_txt).move_to(mmio_box.get_center())

        self.play(FadeIn(pkt, scale=0.5), run_time=0.8)
        # 1. MMIO -> Host Controller
        self.play(pkt.animate.move_to(host_ctrl.get_center()), run_time=1.2)
        # 2. Host Controller -> Disk Controller via I/O Bus
        self.play(pkt.animate.move_to( LEFT * 2.15 + UP * 0.4 ), run_time=1.2)
        self.play(pkt.animate.move_to(disk_ctrl.get_top() + DOWN * 0.35), run_time=1.2)
        self.play(FadeOut(pkt), run_time=0.5)

        # 3. Mechanical transfer between platter & cache while platter spins
        for i in range(4):
            bit_dot = Dot(color=ORANGE, radius=0.09).move_to(mini_platter.get_left())
            self.play(
                Rotate(mini_platter, angle=PI / 2, about_point=mini_platter.get_center(), rate_func=linear),
                bit_dot.animate.move_to(cache_slots[i].get_center()),
                cache_slots[i].animate.set_fill(YELLOW, opacity=0.9),
                run_time=1.2
            )
            self.remove(bit_dot)

        # 4. Fast electronic burst from Cache -> Host Controller
        burst_dots = VGroup(*[Dot(color=GREEN_A, radius=0.09).move_to(s.get_center()) for s in cache_slots])
        self.play(
            burst_dots.animate.arrange(RIGHT, buff=0.15).move_to(host_ctrl.get_center()),
            *[s.animate.set_fill(YELLOW_E, opacity=0.35) for s in cache_slots],
            run_time=1.4
        )
        self.play(FadeOut(burst_dots), Flash(host_ctrl, color=GREEN_A), run_time=0.8)

        # Bottom Callout: Stated vs. Effective Transfer Rate (Page 470 Box)
        rate_box = RoundedRectangle(width=12.6, height=1.55, corner_radius=0.12, color=TEAL_C, fill_color="#0d1b2a", fill_opacity=0.95).move_to(DOWN * 2.45)
        rate_title = Text("REAL-WORLD PERFORMANCE: Stated vs. Effective Disk Transfer Rates", font_size=15, color=TEAL_B, weight=BOLD).next_to(
            rate_box.get_top(), DOWN, buff=0.12, aligned_edge=LEFT
        ).shift(RIGHT * 0.25)

        bar_stated_bg = Rectangle(width=4.5, height=0.26, color=GREY_D, fill_color=GREY_E, fill_opacity=1.0).move_to(LEFT * 2.2 + DOWN * 2.35)
        bar_stated_fill = Rectangle(width=4.2, height=0.26, color=BLUE_B, fill_color=BLUE_C, fill_opacity=0.9).align_to(bar_stated_bg, LEFT).move_to(bar_stated_bg, aligned_edge=LEFT)
        lbl_stated = Text("Stated Rate (Media -> Head): 100%", font_size=13, color=BLUE_B).next_to(bar_stated_bg, LEFT, buff=0.2)

        bar_eff_bg = Rectangle(width=4.5, height=0.26, color=GREY_D, fill_color=GREY_E, fill_opacity=1.0).move_to(LEFT * 2.2 + DOWN * 2.8)
        bar_eff_fill = Rectangle(width=2.7, height=0.26, color=GREEN_B, fill_color=GREEN_C, fill_opacity=0.9).align_to(bar_eff_bg, LEFT).move_to(bar_eff_bg, aligned_edge=LEFT)
        lbl_eff = Text("Effective Rate (Delivered to OS):", font_size=13, color=GREEN_B).next_to(bar_eff_bg, LEFT, buff=0.2)

        rate_note = Text(
            "Published transfer rates measure raw magnetic bit reads\n"
            "at the disk head, which are higher than the effective rate\n"
            "at which logical blocks are delivered to the OS.",
            font_size=13, color=GREY_A, line_spacing=1.2
        ).move_to(RIGHT * 3.3 + DOWN * 2.55)

        self.play(FadeIn(rate_box), Write(rate_title), FadeIn(lbl_stated), Create(bar_stated_bg), FadeIn(lbl_eff), Create(bar_eff_bg), FadeIn(rate_note), run_time=2.5)
        self.play(GrowFromEdge(bar_stated_fill, LEFT), GrowFromEdge(bar_eff_fill, LEFT), run_time=2.5)
        self.wait(6.0)

        self.clear_stage()

    # =========================================================================
    # ACT 4: Solid-State Disks (SSDs) vs. Magnetic Tapes (~52s)
    # =========================================================================
    def act_4_ssd_vs_magnetic_tape(self):
        self.play(
            self.advance_progress(0.63, "ACT 4/6: 10.1.2 SOLID-STATE DISKS (SSDs) VS. 10.1.3 MAGNETIC TAPES"),
            run_time=0.8
        )
        banner = self.build_banner(
            "10.1.2 & 10.1.3", "Solid-State Disks (SSDs) vs. Magnetic Tapes",
            "SLC/MLC Nonvolatile Flash & PCI Cache Tiers vs. Sequential Spools (LTO-5 / SDLT)"
        )
        self.play(FadeIn(banner), run_time=1.2)

        mid_div = Line(UP * 2.0, DOWN * 3.3, color=GREY_D, stroke_width=1.5)
        self.play(Create(mid_div), run_time=0.6)

        # --- LEFT SIDE: 10.1.2 Solid-State Disks (SSDs) ---
        ssd_hdr = Text("10.1.2 Solid-State Disks (SSDs)", font_size=20, color=TEAL_B, weight=BOLD).move_to(LEFT * 3.35 + UP * 1.65)
        pcb = RoundedRectangle(width=3.2, height=1.75, corner_radius=0.1, color=TEAL_C, fill_color="#0d262b", fill_opacity=0.95).move_to(LEFT * 4.6 + UP * 0.45)
        nand_grid = VGroup(*[
            Square(side_length=0.35, color=TEAL_A, fill_color=TEAL_E, fill_opacity=0.75)
            for _ in range(12)
        ]).arrange_in_grid(rows=3, cols=4, buff=0.12).move_to(pcb.get_center())
        pci_pins = VGroup(*[
            Rectangle(width=0.12, height=0.18, color=GOLD_B, fill_color=GOLD_D, fill_opacity=1.0)
            for _ in range(8)
        ]).arrange(RIGHT, buff=0.08).next_to(pcb, DOWN, buff=0)
        pci_lbl = Text("Direct PCI System Bus", font_size=12, color=GOLD_B).next_to(pci_pins, DOWN, buff=0.08)

        # Storage Cache Tier Hierarchy Mini-Diagram
        tier_title = Text("Cache Tiering", font_size=14, color=YELLOW_B, weight=BOLD).move_to(LEFT * 1.65 + UP * 1.15)
        t_ram = RoundedRectangle(width=1.8, height=0.42, corner_radius=0.06, color=GREEN_B, fill_opacity=0.25).move_to(LEFT * 1.65 + UP * 0.7)
        t_ssd = RoundedRectangle(width=1.8, height=0.42, corner_radius=0.06, color=TEAL_B, fill_opacity=0.4).move_to(LEFT * 1.65 + UP * 0.1)
        t_hdd = RoundedRectangle(width=1.8, height=0.42, corner_radius=0.06, color=BLUE_B, fill_opacity=0.25).move_to(LEFT * 1.65 + DOWN * 0.5)
        t_lbls = VGroup(
            Text("Main Memory", font_size=12, color=WHITE).move_to(t_ram),
            Text("SSD Cache Tier", font_size=12, color=TEAL_A, weight=BOLD).move_to(t_ssd),
            Text("Magnetic Disk", font_size=12, color=WHITE).move_to(t_hdd),
        )
        t_arrows = VGroup(
            DoubleArrow(t_ram.get_bottom(), t_ssd.get_top(), buff=0.02, stroke_width=2, color=YELLOW),
            DoubleArrow(t_ssd.get_bottom(), t_hdd.get_top(), buff=0.02, stroke_width=2, color=YELLOW),
        )

        ssd_facts = VGroup(
            Text("• Tech: Battery-backed DRAM or SLC / MLC Flash chips", font_size=13, color=WHITE),
            Text("• Pros: No moving parts (reliable), 0 seek/latency, low power", font_size=13, color=GREEN_B),
            Text("• Cons: Higher cost/MB, lower max capacity, shorter lifespan", font_size=13, color=RED_B),
            Text("• OS Note: Disk-scheduling doesn't apply; formatting does", font_size=13, color=YELLOW_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(LEFT * 3.35 + DOWN * 2.15)

        self.play(
            Write(ssd_hdr), FadeIn(pcb), Create(nand_grid), FadeIn(pci_pins), FadeIn(pci_lbl),
            Write(tier_title), FadeIn(t_ram, t_ssd, t_hdd, t_lbls), Create(t_arrows),
            run_time=3.5
        )
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in ssd_facts], lag_ratio=0.25), run_time=3.5)

        # --- RIGHT SIDE: 10.1.3 Magnetic Tapes ---
        tape_hdr = Text("10.1.3 Magnetic Tapes", font_size=20, color=ORANGE, weight=BOLD).move_to(RIGHT * 3.35 + UP * 1.65)
        deck_box = RoundedRectangle(width=5.4, height=1.9, corner_radius=0.12, color=ORANGE, fill_color="#21150d", fill_opacity=0.92).move_to(RIGHT * 3.35 + UP * 0.35)

        # Dynamic differential spool winding tracker
        wind_progress = ValueTracker(0.0)
        l_center = RIGHT * 1.85 + UP * 0.45
        r_center = RIGHT * 4.85 + UP * 0.45

        spool_left = always_redraw(lambda: VGroup(
            Circle(radius=0.68 - 0.32 * wind_progress.get_value(), color=ORANGE, fill_color=GOLD_E, fill_opacity=0.8),
            Circle(radius=0.18, color=WHITE, fill_color=GREY_C, fill_opacity=1.0),
        ).move_to(l_center))

        spool_right = always_redraw(lambda: VGroup(
            Circle(radius=0.36 + 0.32 * wind_progress.get_value(), color=ORANGE, fill_color=GOLD_E, fill_opacity=0.8),
            Circle(radius=0.18, color=WHITE, fill_color=GREY_C, fill_opacity=1.0),
        ).move_to(r_center))

        spokes_l = VGroup(
            Line(LEFT * 0.5, RIGHT * 0.5, color=WHITE),
            Line(UP * 0.5, DOWN * 0.5, color=WHITE)
        ).move_to(l_center)
        spokes_r = VGroup(
            Line(LEFT * 0.5, RIGHT * 0.5, color=WHITE),
            Line(UP * 0.5, DOWN * 0.5, color=WHITE)
        ).move_to(r_center)

        tape_path = Line(l_center + DOWN * 0.55, r_center + DOWN * 0.55, color=YELLOW_D, stroke_width=4)
        tape_rw_head = RegularPolygon(n=3, color=RED_B, fill_color=RED, fill_opacity=1.0).scale(0.18).next_to(tape_path, DOWN, buff=0.03)
        head_tag = Text("R/W Head", font_size=11, color=RED_B).next_to(tape_rw_head, RIGHT, buff=0.1)

        tape_facts = VGroup(
            Text("• Random access is ~1,000x slower than magnetic disk", font_size=13, color=RED_B),
            Text("• Winding to position takes minutes; writes at disk speeds", font_size=13, color=WHITE),
            Text("• Multi-TB capacity + built-in compression (>2x storage)", font_size=13, color=GREEN_B),
            Text("• Widths: 4, 8, 19mm; 1/4, 1/2 in • Tech: LTO-5 & SDLT", font_size=13, color=YELLOW_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(RIGHT * 3.35 + DOWN * 2.15)

        self.play(
            Write(tape_hdr), FadeIn(deck_box), FadeIn(spool_left), FadeIn(spool_right),
            FadeIn(spokes_l), FadeIn(spokes_r), Create(tape_path), FadeIn(tape_rw_head), FadeIn(head_tag),
            run_time=3.0
        )
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in tape_facts], lag_ratio=0.25), run_time=3.5)

        # Animate simultaneous instant random flash accesses vs slow continuous spool winding
        for idx in [0, 7, 3, 11, 5, 9]:
            self.play(
                Indicate(nand_grid[idx], color=YELLOW, scale_factor=1.25),
                Rotate(spokes_l, angle=-PI, about_point=l_center, rate_func=linear),
                Rotate(spokes_r, angle=-PI, about_point=r_center, rate_func=linear),
                wind_progress.animate.increment_value(1 / 6),
                run_time=1.8
            )
        self.wait(4.0)

        self.clear_stage()

    # =========================================================================
    # ACT 5: Disk Structure — 1D Block Mapping, Bad Sectors & CLV/CAV (~54s)
    # =========================================================================
    def act_5_mapping_and_clv_cav(self):
        self.play(
            self.advance_progress(0.82, "ACT 5/6: 10.2 LOGICAL BLOCK MAPPING, SPARE SECTORS & CLV VS. CAV"),
            run_time=0.8
        )
        banner = self.build_banner(
            "10.2", "Disk Structure: 1D Logical Block Array, Spare Mapping & CLV vs. CAV",
            "512B / 1,024B Logical Blocks • Sector 0 Outermost Cylinder • Defective Sector Substitution"
        )
        self.play(FadeIn(banner), run_time=1.2)

        # --- PART 5A: 1D Logical Block Array & Defective Sector Substitution ---
        lba_title = Text("1D Logical Block Array (512B / 1,024B units):", font_size=15, color=BLUE_B, weight=BOLD).move_to(LEFT * 3.8 + UP * 1.65)
        lba_cells = VGroup()
        for i in range(9):
            is_bad = (i == 4)
            is_spare = (i == 8)
            col = RED_C if is_bad else (GREEN_C if is_spare else BLUE_C)
            rect = Square(side_length=0.58, color=col, fill_color="#162238", fill_opacity=0.95)
            lbl_str = "S0" if i == 0 else ("BAD" if is_bad else ("SPR" if is_spare else f"L{i}"))
            t = Text(lbl_str, font_size=12, color=WHITE, weight=BOLD).move_to(rect)
            lba_cells.add(VGroup(rect, t))
        lba_cells.arrange(RIGHT, buff=0.08).next_to(lba_title, RIGHT, buff=0.25)

        map_rule = Text(
            "Sequential Mapping: Sector 0 (1st track, outermost cylinder) -> Track -> Cylinder -> Innermost Cylinder",
            font_size=13, color=GREY_A
        ).next_to(lba_cells, DOWN, buff=0.16).set_x(0)

        self.play(Write(lba_title), Create(lba_cells), FadeIn(map_rule), run_time=2.5)

        # Animate Bad Sector Remapping Curve (L4 defective -> substituted by Spare Sector SPR)
        remap_arc = CurvedArrow(lba_cells[4].get_top(), lba_cells[8].get_top(), angle=-PI / 3, color=YELLOW_B, stroke_width=3)
        remap_lbl = Text("Defective Sector Remapped to Spare", font_size=12, color=YELLOW_B).next_to(remap_arc, UP, buff=0.05)
        self.play(Indicate(lba_cells[4], color=RED), Create(remap_arc), FadeIn(remap_lbl), Indicate(lba_cells[8], color=GREEN), run_time=2.8)

        # --- PART 5B: Live Kinematic Comparison — CLV vs. CAV ---
        clv_c = LEFT * 3.3 + DOWN * 1.25
        cav_c = RIGHT * 3.3 + DOWN * 1.25

        clv_hdr = Text("CLV: Constant Linear Velocity", font_size=17, color=GREEN_B, weight=BOLD).move_to(clv_c + UP * 1.8)
        cav_hdr = Text("CAV: Constant Angular Velocity", font_size=17, color=YELLOW_B, weight=BOLD).move_to(cav_c + UP * 1.8)

        def build_zoned_platter(center, counts, cols):
            disk = VGroup()
            radii = [(0.35, 0.72), (0.72, 1.08), (1.08, 1.45)]
            for idx, ((r_in, r_out), n_s) in enumerate(zip(radii, counts)):
                da = TAU / n_s
                for s in range(n_s):
                    w = AnnularSector(
                        inner_radius=r_in, outer_radius=r_out, angle=da, start_angle=s * da,
                        fill_color=cols[idx], fill_opacity=0.6, stroke_color=WHITE, stroke_width=0.9
                    ).shift(center)
                    disk.add(w)
            disk.add(Circle(radius=0.16, color=WHITE, fill_color=GREY_A, fill_opacity=1.0).move_to(center))
            return disk

        # CLV: Outer zone holds ~40% more sectors than inner zone (uniform bit density)
        clv_disk = build_zoned_platter(clv_c, counts=[8, 11, 14], cols=[TEAL_E, TEAL_C, GREEN_D])
        # CAV: Constant sectors per track angle (bit density decreases from inner to outer)
        cav_disk = build_zoned_platter(cav_c, counts=[8, 8, 8], cols=[GOLD_E, YELLOW_D, ORANGE])

        clv_head = Dot(color=RED_A, radius=0.09).move_to(clv_c + RIGHT * 1.26)
        cav_head = Dot(color=RED_A, radius=0.09).move_to(cav_c + RIGHT * 1.26)

        clv_rpm_tracker = ValueTracker(500)
        cav_rpm_tracker = ValueTracker(7200)

        clv_Readout = always_redraw(lambda: Text(
            f"Head Speed: {int(clv_rpm_tracker.get_value())} RPM (Increases Inward)",
            font_size=13, color=GREEN_A
        ).move_to(clv_c + DOWN * 1.72))

        cav_Readout = always_redraw(lambda: Text(
            f"Head Speed: {int(cav_rpm_tracker.get_value())} RPM (Constant Speed)",
            font_size=13, color=YELLOW_A
        ).move_to(cav_c + DOWN * 1.72))

        clv_sub = Text("Uniform bit density • +40% outer sectors • CD-ROM / DVD-ROM", font_size=12, color=GREY_B).move_to(clv_c + DOWN * 2.02)
        cav_sub = Text("Inner density > Outer density • Constant data rate • Hard Disks", font_size=12, color=GREY_B).move_to(cav_c + DOWN * 2.02)

        self.play(
            Write(clv_hdr), Write(cav_hdr),
            FadeIn(clv_disk), FadeIn(cav_disk),
            FadeIn(clv_head), FadeIn(cav_head),
            FadeIn(clv_Readout), FadeIn(cav_Readout),
            FadeIn(clv_sub), FadeIn(cav_sub),
            run_time=3.0
        )

        # Animate heads moving from Outer Zone -> Middle Zone -> Inner Zone while CLV accelerates RPM
        self.play(
            Rotate(clv_disk, angle=TAU * 1.2, about_point=clv_c, rate_func=linear),
            Rotate(cav_disk, angle=TAU * 2.0, about_point=cav_c, rate_func=linear),
            clv_head.animate.move_to(clv_c + RIGHT * 0.9),
            cav_head.animate.move_to(cav_c + RIGHT * 0.9),
            clv_rpm_tracker.animate.set_value(950),
            run_time=4.5
        )
        self.play(
            Rotate(clv_disk, angle=TAU * 2.5, about_point=clv_c, rate_func=linear),
            Rotate(cav_disk, angle=TAU * 2.0, about_point=cav_c, rate_func=linear),
            clv_head.animate.move_to(clv_c + RIGHT * 0.53),
            cav_head.animate.move_to(cav_c + RIGHT * 0.53),
            clv_rpm_tracker.animate.set_value(1600),
            run_time=4.5
        )
        self.wait(4.5)

        self.clear_stage()

    # =========================================================================
    # ACT 6: Disk Attachment — Host-Attached, NAS & SAN (~54s)
    # =========================================================================
    def act_6_attachment_nas_san(self):
        self.play(
            self.advance_progress(1.0, "ACT 6/6: 10.3 HOST-ATTACHED, NAS (FIG 10.2) & STORAGE-AREA NETWORK (SAN)"),
            run_time=0.8
        )
        banner = self.build_banner(
            "10.3 & 10.4", "Disk Attachment Topologies: Host-Attached, NAS & SAN",
            "ATA/SATA/FC-AL • NAS via NFS/CIFS/iSCSI over LAN • SAN Private Switched Fabric & Dynamic Allocation"
        )
        self.play(FadeIn(banner), run_time=1.2)

        def node_box(txt, w=1.55, h=0.52, col=BLUE_C, fill="#162238"):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.08, color=col, fill_color=fill, fill_opacity=0.95)
            t = Text(txt, font_size=13, color=WHITE, weight=BOLD).move_to(r)
            return VGroup(r, t)

        # --- COLUMN 1: 10.3.1 Host-Attached Storage ---
        c1_x = LEFT * 4.45
        c1_hdr = Text("10.3.1 Host-Attached", font_size=18, color=TEAL_B, weight=BOLD).move_to(c1_x + UP * 1.65)
        h_pc = node_box("Workstation / Host", w=2.3, col=TEAL_C).move_to(c1_x + UP * 0.9)
        h_d1 = node_box("Drive 0 (IDE/SATA)", w=2.3, col=BLUE_C).move_to(c1_x + DOWN * 0.1)
        h_d2 = node_box("FC-AL Loop / RAID", w=2.3, col=PURPLE_B).move_to(c1_x + DOWN * 1.0)
        h_lines = VGroup(
            DoubleArrow(h_pc.get_bottom(), h_d1.get_top(), buff=0.05, stroke_width=2.5, color=TEAL_A),
            DoubleArrow(h_d1.get_bottom(), h_d2.get_top(), buff=0.05, stroke_width=2.5, color=PURPLE_A),
        )
        c1_bullets = VGroup(
            Text("• IDE/ATA: Max 2 drives/bus", font_size=12, color=WHITE),
            Text("• SATA: Simplified cabling", font_size=12, color=WHITE),
            Text("• FC Switched: 24-bit address", font_size=12, color=TEAL_A),
            Text("• FC-AL Loop: Up to 126 devices", font_size=12, color=PURPLE_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(c1_x + DOWN * 2.2)

        # --- COLUMN 2: 10.3.2 Network-Attached Storage (Figure 10.2) ---
        c2_x = ORIGIN
        c2_hdr = Text("10.3.2 NAS (Figure 10.2)", font_size=18, color=YELLOW_B, weight=BOLD).move_to(c2_x + UP * 1.65)
        lan_cloud = Ellipse(width=2.1, height=1.15, color=BLUE_B, fill_color=BLUE_E, fill_opacity=0.45).move_to(c2_x + UP * 0.05)
        lan_lbl = Text("LAN / WAN\n(TCP/UDP/IP)", font_size=12, color=WHITE, weight=BOLD).move_to(lan_cloud)

        nas_1 = node_box("NAS 1", w=1.05, h=0.45, col=YELLOW_C).move_to(c2_x + LEFT * 1.55 + UP * 0.75)
        nas_2 = node_box("NAS 2", w=1.05, h=0.45, col=YELLOW_C).move_to(c2_x + LEFT * 1.55 + DOWN * 0.65)
        cli_1 = node_box("Client", w=1.05, h=0.45, col=GREEN_C).move_to(c2_x + RIGHT * 1.55 + UP * 0.85)
        cli_2 = node_box("Client", w=1.05, h=0.45, col=GREEN_C).move_to(c2_x + RIGHT * 1.55 + UP * 0.05)
        cli_3 = node_box("Client", w=1.05, h=0.45, col=GREEN_C).move_to(c2_x + RIGHT * 1.55 + DOWN * 0.75)

        nas_wires = VGroup(
            Line(nas_1.get_right(), lan_cloud.get_left() + UP * 0.2, color=GREY_B),
            Line(nas_2.get_right(), lan_cloud.get_left() + DOWN * 0.2, color=GREY_B),
            Line(lan_cloud.get_right() + UP * 0.25, cli_1.get_left(), color=GREY_B),
            Line(lan_cloud.get_right(), cli_2.get_left(), color=GREY_B),
            Line(lan_cloud.get_right() + DOWN * 0.25, cli_3.get_left(), color=GREY_B),
        )
        c2_bullets = VGroup(
            Text("• RPCs: NFS (UNIX) / CIFS (Win)", font_size=12, color=WHITE),
            Text("• iSCSI: SCSI over IP network", font_size=12, color=YELLOW_A),
            Text("• Drawback: Storage I/O consumes", font_size=12, color=RED_B),
            Text("  LAN bandwidth & adds latency!", font_size=12, color=RED_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(c2_x + DOWN * 2.2)

        # --- COLUMN 3: 10.3.3 Storage-Area Network (SAN) ---
        c3_x = RIGHT * 4.45
        c3_hdr = Text("10.3.3 Storage-Area Network", font_size=18, color=PURPLE_B, weight=BOLD).move_to(c3_x + UP * 1.65)
        san_sw = RoundedRectangle(width=1.45, height=1.65, corner_radius=0.15, color=PURPLE_B, fill_color="#2a124c", fill_opacity=0.85).move_to(c3_x + UP * 0.05)
        san_sw_lbl = Text("SAN\nSwitch\n(FC / IB)", font_size=12, color=WHITE, weight=BOLD).move_to(san_sw)

        srv_1 = node_box("Server 1", w=1.15, h=0.45, col=GREEN_C).move_to(c3_x + LEFT * 1.55 + UP * 0.65)
        srv_2 = node_box("Server 2", w=1.15, h=0.45, col=GREEN_C).move_to(c3_x + LEFT * 1.55 + DOWN * 0.55)
        arr_1 = node_box("Array 1", w=1.15, h=0.45, col=ORANGE).move_to(c3_x + RIGHT * 1.55 + UP * 0.65)
        arr_2 = node_box("Array 2", w=1.15, h=0.45, col=ORANGE).move_to(c3_x + RIGHT * 1.55 + DOWN * 0.55)

        san_wires = VGroup(
            Line(srv_1.get_right(), san_sw.get_left() + UP * 0.35, color=PURPLE_A),
            Line(srv_2.get_right(), san_sw.get_left() + DOWN * 0.35, color=PURPLE_A),
            Line(san_sw.get_right() + UP * 0.35, arr_1.get_left(), color=PURPLE_A),
            Line(san_sw.get_right() + DOWN * 0.35, arr_2.get_left(), color=PURPLE_A),
        )
        c3_bullets = VGroup(
            Text("• Private storage protocol fabric", font_size=12, color=WHITE),
            Text("• Dynamic storage allocation", font_size=12, color=GREEN_B),
            Text("• Interconnects: FC, iSCSI,", font_size=12, color=PURPLE_A),
            Text("  & high-speed InfiniBand", font_size=12, color=PURPLE_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(c3_x + DOWN * 2.2)

        # Build all 3 columns progressively
        self.play(Write(c1_hdr), FadeIn(h_pc, h_d1, h_d2), Create(h_lines), FadeIn(c1_bullets), run_time=3.5)
        self.play(
            Write(c2_hdr), FadeIn(lan_cloud, lan_lbl, nas_1, nas_2, cli_1, cli_2, cli_3),
            Create(nas_wires), FadeIn(c2_bullets),
            run_time=3.5
        )
        self.play(
            Write(c3_hdr), FadeIn(san_sw, san_sw_lbl, srv_1, srv_2, arr_1, arr_2),
            Create(san_wires), FadeIn(c3_bullets),
            run_time=3.5
        )

        # Simulate LAN Congestion on NAS vs Dynamic Allocation on SAN
        nas_pkts = VGroup(*[Dot(color=RED_A, radius=0.07).move_to(nas_1.get_right()) for _ in range(4)])
        san_alloc_beam = Line(arr_2.get_left(), srv_1.get_right(), color=GREEN_A, stroke_width=5)
        alloc_tag = Text("Dynamic Storage Allocated!", font_size=12, color=GREEN_A, weight=BOLD).next_to(san_sw, UP, buff=0.15)

        self.play(
            lan_cloud.animate.set_color(RED_B),
            nas_pkts.animate.arrange(RIGHT, buff=0.1).move_to(lan_cloud.get_center()),
            run_time=2.5
        )
        self.play(
            Create(san_alloc_beam), FadeIn(alloc_tag),
            Indicate(srv_1, color=GREEN_A), Indicate(arr_2, color=GREEN_A),
            run_time=3.0
        )
        self.wait(3.0)

        # Final 10.4 Disk Scheduling Bridge Banner
        sched_banner = RoundedRectangle(
            width=11.5, height=0.85, corner_radius=0.12, color=BLUE_B, fill_color="#0f172a", fill_opacity=0.98
        ).move_to(DOWN * 3.05)
        sched_txt = Text(
            "Up Next in 10.4 Disk Scheduling: OS scheduling of disk I/O requests to minimize seek time & maximize bandwidth",
            font_size=14, color=TEAL_A, weight=BOLD
        ).move_to(sched_banner)

        self.play(FadeIn(sched_banner, shift=UP * 0.2), Write(sched_txt), run_time=2.5)
        self.wait(5.0)

        self.clear_stage()