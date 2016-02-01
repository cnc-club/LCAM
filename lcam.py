#!/usr/bin/env python

# @(#)$Id: gl_gtk_app.py,v 1.2 2011/06/20 01:50:09 wiles Exp $

'''An example of connecting the OpenGL interface to a GTK drawable.

The most interesting code is in the GtkGlDrawingArea class.

To test the code you'll need 2 images.  See the documentation for
texture_1_fname'''

import string
__version__ = string.split('$Revision: 1.2 $')[1]
__date__ = string.join(string.split('$Date: 2011/06/20 01:50:09 $')[1:3], ' ')
__author__ = 'Dale Wiles <Dale.Wiles@Gmail.Remove.Com>'

import pygtk
pygtk.require('2.0')
import gobject
import gtk
import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *

#
# The only reason these variables are global is to make them easier
# to play with.
#

# The animation update in milliseconds.
# Set it to 0 to update as fast as possible.
animate_rate_ms = 10

# The texture image file names.
# These need to be any file that GTK can read.  I tend to use PNGs
# that are around 256x256.
texture_1_fname = "tex1.png"
texture_2_fname = "tex2.bmp"

# Rotations for cube.
cube_rotate_x_rate = 0.2
cube_rotate_y_rate = 0.2
cube_rotate_z_rate = 0.2

# Rotation rates for the tetrahedron.
tet_x_rate = 0.0
tet_y_rate = 1.0
tet_z_rate = 0.5
tet_rotate_step = 1.0

#: GlStuff #:
#
# This is pretty much generic OpenGL code.
#
# It produces a couple of shapes and spins them.  Any other OpenGL
# code would do fit the bill as well as this does.
#
# Much of this code was derived, or at least inspired, by a port of
# the NeHe open GL tutorial.  Giving proper credit, this was the
# comment in the file that I used as a template.
#
#   Ported to PyOpenGL 2.0 by Tarn Weisner Burton 10May2001
#
#   This code was created by Richard Campbell '99 (ported to
#   Python/PyOpenGL by John Ferguson 2000)
#
#   The port was based on the lesson5 tutorial module by Tony Colston
#   (tonetheman@hotmail.com).
#
#   If you've found this code useful, please let me know (email
#   John Ferguson at hakuin@voicenet.com).
#
#   See original source and C based tutorial at http:#nehe.gamedev.net
#
class GlStuff():
    # This is just a container class to hold all the GL stuff in one place.
    def __init__(self):
        # Create an double buffered RGB mode with depth checking.
        # This throws an exception if it fails.  (If the video card
        # can't handle it.)
        self.glconfig = gtk.gdkgl.Config(mode = (gtk.gdkgl.MODE_RGB |
                                                 gtk.gdkgl.MODE_DOUBLE |
                                                 gtk.gdkgl.MODE_DEPTH))

        # The textures can't be created until the window is up.
        self.texture_1 = self.texture_2 = None

        self.x_rot = self.y_rot = self.z_rot = 0.0
        self.tet_rotate = 0.0

    def is_set_up(self):
        return self.texture_1 is not None

    def set_up(self, width, height):
        """Set up the 'once a program' GL stuff."""
        self.load_textures()

        glClearColor(0.0, 0.0, 0.0, 0.0) # Clear to black.
        glClearDepth(1.0)       # Enable clearing of the depth buffer
        glDepthFunc(GL_LESS)    # The type of depth test to do
        glEnable(GL_DEPTH_TEST) # Turn on depth testing.
        glShadeModel(GL_SMOOTH) # Enables smooth color shading

        self.set_projection_matrix(width, height)

    def redraw_contents(self):
        def redraw_cube():
            glLoadIdentity()           # Reset The View
            glTranslatef(-1.0, 0.0, -6.0) # Move Into The Screen

            # Rotate the cube on X, Y and Z.
            glRotatef(self.x_rot, 1.0, 0.0, 0.0)
            glRotatef(self.y_rot, 0.0, 1.0, 0.0)
            glRotatef(self.z_rot, 0.0, 0.0, 1.0)

            self.draw_2textured_cube(self.texture_1, self.texture_2)

            # Move the cube for the next draw.
            global cube_rotate_x_rate, cube_rotate_y_rate, cube_rotate_z_rate
            self.x_rot = self.x_rot + cube_rotate_x_rate
            self.y_rot = self.y_rot + cube_rotate_y_rate
            self.z_rot = self.z_rot + cube_rotate_z_rate

        def redraw_tet():
            # Move it in to place.
            glLoadIdentity()
            glTranslatef(1.0, 0.0, -6.0)

            # Rotate X, Y and Z all at once.
            global tet_x_rate, tet_y_rate, tet_z_rate
            glRotatef(self.tet_rotate, tet_x_rate, tet_y_rate, tet_z_rate)

            self.draw_tetrahedron()

            global tet_rotate_step
            self.tet_rotate = self.tet_rotate + tet_rotate_step

        #: Body #:
        # Clear the screen and the depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        redraw_cube()
        redraw_tet()

    def resize_viewport(self, width, height):
        """The user has resized the window so resize the view port to match."""
        if height == 0: height = 1 # Prevent divide by 0 errors.

        glViewport(0, 0, width, height)

        self.set_projection_matrix(width, height)

    def set_projection_matrix(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Set up a nice 45 degree perspective.
        gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def draw_2textured_cube(self, tex_1, tex_2):
        """Draw a cube using 2 different textures."""
        def draw_first_3_faces(texture):
            # Set the 2D texture to the texture we requested.
            glBindTexture(GL_TEXTURE_2D, texture)

            glBegin(GL_QUADS)

            # For the front face, we tack the upper left corner to the upper
            # left corner of the quad.  Then we move to upper right, lower
            # right and lower left.  If we exchange the 0.0s and the 1.0s in
            # glTexCoord2f, the front face gets drawn upside down.
            glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
            glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
            glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
            glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)

            # Back.
            glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
            glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
            glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
            glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)

            # Top.
            glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
            glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)
            glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)
            glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)

            glEnd()

        def draw_last_3_faces(texture):
            glBindTexture(GL_TEXTURE_2D, texture)

            glBegin(GL_QUADS)

            # Bottom.
            glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)
            glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)
            glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
            glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)

            # Right.
            glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)
            glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
            glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
            glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)

            # Left.
            glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
            glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
            glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)
            glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)

            glEnd()

        #: Body #:
        glEnable(GL_TEXTURE_2D)     # Start using textures to draw.
        draw_first_3_faces(tex_1)
        draw_last_3_faces(tex_2)
        glDisable(GL_TEXTURE_2D)    # Stop using textures when drawing.

    def draw_tetrahedron(self):
        # Start with 4 triangles for the top of the pyramid.
        glBegin(GL_TRIANGLES);

        # Front.
        # Each Red/Green/Blue contribution goes from 0.0 (no contribution)
        # to 1.0 (full contribution).  "1.0, 0.0, 0.0" is red.
        #   "1.0, 0.0, 1.0" is purple (red & blue)
        glColor3f(1.0, 0.0, 0.0); glVertex3f( 0.0,  1.0, 0.0)
        glColor3f(0.0, 1.0, 0.0); glVertex3f(-1.0, -1.0, 1.0)
        glColor3f(0.0, 0.0, 1.0); glVertex3f( 1.0, -1.0, 1.0)

        # Right.
        glColor3f(1.0,0.0,0.0); glVertex3f( 0.0, 1.0, 0.0)
        glColor3f(0.0,0.0,1.0); glVertex3f( 1.0,-1.0, 1.0)
        glColor3f(0.0,1.0,0.0); glVertex3f( 1.0,-1.0, -1.0)

        # Back.
        glColor3f(1.0,0.0,0.0); glVertex3f( 0.0, 1.0, 0.0)
        glColor3f(0.0,1.0,0.0); glVertex3f( 1.0,-1.0, -1.0)
        glColor3f(0.0,0.0,1.0); glVertex3f(-1.0,-1.0, -1.0)

        # Left.
        glColor3f(1.0,0.0,0.0); glVertex3f( 0.0, 1.0, 0.0)
        glColor3f(0.0,0.0,1.0); glVertex3f(-1.0,-1.0,-1.0)
        glColor3f(0.0,1.0,0.0); glVertex3f(-1.0,-1.0, 1.0)

        glEnd();

        # Cap the bottom off with a square, making sure the colors
        # line up with the pyramid.
        glBegin(GL_QUADS)

        glColor3f(0.0,0.0,1.0); glVertex3f(-1.0, -1.0, -1.0)
        glColor3f(0.0,1.0,0.0); glVertex3f( 1.0, -1.0, -1.0)
        glColor3f(0.0,0.0,1.0); glVertex3f( 1.0, -1.0,  1.0)
        glColor3f(0.0,1.0,0.0); glVertex3f(-1.0, -1.0,  1.0)

        glEnd()

    def load_textures(self):
        def texture_from_image(ifname):
            """Read in an image and convert it to an OpenGL format
byte string.

This function reverses the line ordering in a GTK image in to an
OpenGL image.

GTK images are loaded in to memory with the last line of the image being
the first line in pixel memory.  OpenGL wants the first line of the image
to be the first line in pixel memory.

This was written so that I didn't have to include the 'Python Image Library'
for one function.  It works for the files that I've tried it out on.

If you run into an image in the wild that it fails on, let me know."""

            # This was the original PIL code.
            # image = open(ifname)
            # image_width = image.size[0]
            # image_height = image.size[1]
            # image = image.tostring("raw", "RGBX", 0, -1)

            gtk_image = gtk.Image()
            gtk_image.set_from_file(ifname)
            # Force it into a Alpha channel pixbuf because the GL code
            # that called this is expecting an alpha channel.
            gtk_image_pb = gtk_image.get_pixbuf().add_alpha(False, 0, 0, 0)

            image_width = gtk_image_pb.get_width()
            image_height = gtk_image_pb.get_height()

            # The first line in a GL Texture is the last line in a
            # pixbuf image, so reverse the lines of in the pixbuf.
            num_rows = gtk_image_pb.get_height()
            row_stride = gtk_image_pb.get_rowstride()
            bytes_per_line = gtk_image_pb.get_width() \
                * gtk_image_pb.get_n_channels()
            end_point = (num_rows - 1) * row_stride

            gtk_pixels = gtk_image_pb.get_pixels()
            gl_pixels = b''
            for row in range(0, num_rows):
              gl_pixels = gl_pixels \
                  + gtk_pixels[end_point:end_point + bytes_per_line:1]
              end_point = end_point - row_stride

            return (gl_pixels, image_width, image_height)

        #: Body #:
        # If you want to free the textures before the program exits, use
        #   glDeleteTextures([self.texture_1, self.texture_2])
        self.texture_1, self.texture_2 = glGenTextures(2)

        global texture_1_fname, texture_2_fname
        for x in [ (self.texture_1, texture_1_fname),
                   (self.texture_2, texture_2_fname) ]:
            tx_id, fname = x

            glBindTexture(GL_TEXTURE_2D, tx_id)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

            image, ix, iy = texture_from_image(fname)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                         GL_RGBA, GL_UNSIGNED_BYTE, image)

            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

#: GtkGlDrawingArea #:
#
# This is the code that ties OpenGL to GTK.
#
# The only real points of interest are
# gtk.gtkgl.DrawingArea/self.gl_stuff.glconfig constructor and the
# connect_gl() function.
#
class GtkGlDrawingArea(gtk.gtkgl.DrawingArea):
    def __init__(self):
        # Allocate the GL guts and gore.
        self.gl_stuff = GlStuff()

        # Associate GL with this specific GTK window.
        super(GtkGlDrawingArea, self).__init__(self.gl_stuff.glconfig)

        # Keep track of which drawable is currently receiving OpenGL
        # commands.  (See connect_gl())
        self.last_gldrawable = None

        # The rest of this function is regular GTK stuff.

        # Create a reasonable minimum size.  It can be made larger,
        # but not smaller, by the user.  This is optional.
        self.set_size_request(640, 480)

        self.connect('configure_event', self.resize_cb)
        self.connect('expose_event', self.expose_cb)
        self.connect('map_event', self.map_cb)

	self.connect('button-press-event', self.mouse_press)
	self.connect('button-release-event', self.mouse_release)
	
        # We don't use 'unmap' here because you don't always get
        # an unmap signal on shutdown.
        self.connect_after('unrealize', self.unrealize_cb)

        # Read from the keyboard.
        self.set_flags(gtk.HAS_FOCUS | gtk.CAN_FOCUS)
        self.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.connect('key_press_event', self.key_cb)

    # A note for all the callbacks, because we subclass
    # gtk.gtkgl.DrawingArea and handle all the events internally
    # self == gl_area.  If we were to hook up the GTK to call functions
    # in ApplicationMainWindowDemo class then self would be the
    # ApplicationMainWindowDemo instance and gl_area would be an instance
    # of this class.
    #
    # There is nothing GL specific about this, but it bares pointing out.
    def key_cb(self, gl_area, event):
        # Keysym names are listed gdkkeysyms.h source code that comes
        # with GTK.
        if event.keyval == gtk.keysyms.Escape:
            gtk.main_quit()
        # print "key: ", (event.state & gtk.gdk.SHIFT_MASK) != 0

        return True

    def resize_cb(self, gl_area, event):
        if not self.connect_gl(gl_area): return

        x, y, width, height = gl_area.get_allocation()
        self.gl_stuff.resize_viewport(width, height)

        self.disconnect_gl()

        return True

    def map_cb(self, gl_area, event):
        """Hook up an reoccurring screen update to produce animation.

At this point the window actually exists as a real window so it can
start getting updates."""

        global animate_rate_ms
        if animate_rate_ms > 0:
            # Update the screen every N milliseconds.
            self.update_id = \
                gobject.timeout_add(animate_rate_ms, self.trigger_redraw)
        else:
            # Update every chance you get.  This is useful for seeing
            # the top speed of your update code.
            self.update_id = gobject.idle_add(self.trigger_redraw)

        return True

    def unrealize_cb(self, gl_area):
        # Remove the timer/idle so it doesn't fire on a partly
        # closed window.
        gobject.source_remove(self.update_id)

        return True

    def trigger_redraw(self):
        """Force the entire GL window to be redrawn"""
        self.window.invalidate_rect(self.allocation, False)
        self.window.process_updates(False)

        return True

    def expose_cb(self, gl_area, event):
        # Because the first expose event occurs before the first map
        # event, check to see that GL is actually set up before using it.
        # Abstract the "if init" code.
        if not self.gl_stuff.is_set_up():
            x, y, width, height = gl_area.get_allocation()
            self.gl_stuff.set_up(width, height)

        if not self.connect_gl(gl_area): return

        self.gl_stuff.redraw_contents()

        self.swap_gl_buffers()

        self.disconnect_gl()

        return True

    #
    # These 3 functions deal with getting to and handling the low level
    # GL access.
    #
    # A built in assertion is that we only hold one GL access at a time.
    # This example has no problem with that, but more elaborate code might.
    # I have no idea how handling multiple accesses is done.
    #
    def connect_gl(self, gl_area):
        """Let the underlying OpenGL library know this drawable should be drawn to.

You'll notice that GL functions don't include where they're writing too.
That information is kept within the bowels of OpenGL.  This function
tells OpenGL that the buffer managed by this drawable should be the
target of OpenGL's machinations.

Return True if the GL buffer was aquired, False otherwise."""
        assert self.last_gldrawable is None, \
            "Attempt to connect a drawable twice"

        glcontext = gl_area.get_gl_context()
        gldrawable = gl_area.get_gl_drawable()

        if gldrawable.gl_begin(glcontext):
            self.last_gldrawable = gldrawable
            return True
        else:
            return False

    def disconnect_gl(self):
        """Release the GL buffer aquired by connect_gl()"""
        assert self.last_gldrawable is not None, \
            "The drawable was disconnected before it was connected"

        self.last_gldrawable.gl_end()
        self.last_gldrawable = None

    def swap_gl_buffers(self):
        """Swap the displayed buffer with the one that has been drawn on."""
        assert self.last_gldrawable is not None, \
            "drawable was disconnected before connection"

        self.last_gldrawable.swap_buffers()

#: Appwindow.py #:
#
# This is just the "appwindow.py" demo program that comes with the pygtk
# source code.
#
# The text buffer and scroll window in the original is replace with
# a GtkGlDrawingArea.
#

'''Application main window

Demonstrates a typical application window, with menubar, toolbar, statusbar.'''
# pygtk version: Maik Hertha <maik.hertha@berlin.de>
(
  COLOR_RED,
  COLOR_GREEN,
  COLOR_BLUE
) = range(3)

(
  SHAPE_SQUARE,
  SHAPE_RECTANGLE,
  SHAPE_OVAL,
) = range(3)

ui_info = \
'''<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menuitem action='New'/>
      <menuitem action='Open'/>
      <menuitem action='Save'/>
      <menuitem action='SaveAs'/>
      <separator/>
      <menuitem action='Quit'/>
    </menu>
    <menu action='PreferencesMenu'>
      <menu action='ColorMenu'>
        <menuitem action='Red'/>
        <menuitem action='Green'/>
        <menuitem action='Blue'/>
      </menu>
      <menu action='ShapeMenu'>
        <menuitem action='Square'/>
        <menuitem action='Rectangle'/>
        <menuitem action='Oval'/>
      </menu>
      <menuitem action='Bold'/>
    </menu>
    <menu action='HelpMenu'>
      <menuitem action='About'/>
    </menu>
  </menubar>
  <toolbar  name='ToolBar'>
    <toolitem action='Open'/>
    <toolitem action='Quit'/>
    <separator/>
    <toolitem action='Logo'/>
  </toolbar>
</ui>'''


# It's totally optional to do this, you could just manually insert icons
# and have them not be themeable, especially if you never expect people
# to theme your app.
def register_stock_icons():
    ''' This function registers our custom toolbar icons, so they
        can be themed.
    '''
    items = [('demo-gtk-logo', '_GTK!', 0, 0, '')]
    # Register our stock items
    gtk.stock_add(items)

    # Add our custom icon factory to the list of defaults
    factory = gtk.IconFactory()
    factory.add_default()

    import os
    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)

        # Register icon to accompany stock item

        # The gtk-logo-rgb icon has a white background, make it transparent
        # the call is wrapped to (gboolean, guchar, guchar, guchar)
        transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
        icon_set = gtk.IconSet(transparent)
        factory.add('demo-gtk-logo', icon_set)

    except gobject.GError, error:
        print 'failed to load GTK logo for toolbar'

class ApplicationMainWindowDemo(gtk.Window):
    def __init__(self, parent=None):
        register_stock_icons()

        # Create the toplevel window
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(200, 200)

        merge = gtk.UIManager()
        self.set_data("ui-manager", merge)
        merge.insert_action_group(self.__create_action_group(), 0)
        self.add_accel_group(merge.get_accel_group())

        try:
            mergeid = merge.add_ui_from_string(ui_info)
        except gobject.GError, msg:
            print "building menus failed: %s" % msg
        bar = merge.get_widget("/MenuBar")
        bar.show()

        table = gtk.Table(1, 4, False)
        self.add(table)

        table.attach(bar,
            # X direction #          # Y direction
            0, 1,                      0, 1,
            gtk.EXPAND | gtk.FILL,     0,
            0,                         0);

        bar = merge.get_widget("/ToolBar")
        bar.set_tooltips(True)
        bar.show()
        table.attach(bar,
            # X direction #       # Y direction
            0, 1,                   1, 2,
            gtk.EXPAND | gtk.FILL,  0,
            0,                      0)

        # ORIGINAL: Replaced with a GL window.
        # Create document
        #sw = gtk.ScrolledWindow()
        #sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        #sw.set_shadow_type(gtk.SHADOW_IN)

        contents = GtkGlDrawingArea()

        table.attach(contents, # ORIGINAL: was sw.
            # X direction           Y direction
            0, 1,                   2, 3,
            gtk.EXPAND | gtk.FILL,  gtk.EXPAND | gtk.FILL,
            0,                      0)

        # ORIGINAL
        # contents = gtk.TextView()
        contents.grab_focus()

        # ORIGINAL
        # sw.add (contents)

        # Create statusbar
        self.statusbar = gtk.Statusbar()
        table.attach(self.statusbar,
            # X direction           Y direction
            0, 1,                   3, 4,
            gtk.EXPAND | gtk.FILL,  0,
            0,                      0)

        # ORIGINAL
        # Show text widget info in the statusbar
        #buffer = contents.get_buffer()
        #buffer.connect("changed", self.update_statusbar)
        #mark_set_callback = (lambda buffer, new_location, mark:
        #    self.update_statusbar(buffer))

        # ORIGINAL
        # cursor moved
        #buffer.connect("mark_set", mark_set_callback)

        self.connect("window_state_event", self.update_resize_grip)
        # ORIGINAL
        # self.update_statusbar(buffer)

        self.show_all()

    def __create_action_group(self):
        # GtkActionEntry
        entries = (
          ( "FileMenu", None, "_File" ),               # name, stock id, label
          ( "PreferencesMenu", None, "_Preferences" ), # name, stock id, label
          ( "ColorMenu", None, "_Color"  ),            # name, stock id, label
          ( "ShapeMenu", None, "_Shape" ),             # name, stock id, label
          ( "HelpMenu", None, "_Help" ),               # name, stock id, label
          ( "New", gtk.STOCK_NEW,                      # name, stock id
            "_New", "<control>N",                      # label, accelerator
            "Create a new file",                       # tooltip
            self.activate_action ),
          ( "Open", gtk.STOCK_OPEN,                    # name, stock id
            "_Open","<control>O",                      # label, accelerator
            "Open a file",                             # tooltip
            self.activate_action ),
          ( "Save", gtk.STOCK_SAVE,                    # name, stock id
            "_Save","<control>S",                      # label, accelerator
            "Save current file",                       # tooltip
            self.activate_action ),
          ( "SaveAs", gtk.STOCK_SAVE,                  # name, stock id
            "Save _As...", None,                       # label, accelerator
            "Save to a file",                          # tooltip
            self.activate_action ),
          ( "Quit", gtk.STOCK_QUIT,                    # name, stock id
            "_Quit", "<control>Q",                     # label, accelerator
            "Quit",                                    # tooltip
            self.activate_action ),
          ( "About", None,                             # name, stock id
            "_About", "<control>A",                    # label, accelerator
            "About",                                   # tooltip
            self.activate_about ),
          ( "Logo", "demo-gtk-logo",                   # name, stock id
             None, None,                              # label, accelerator
            "GTK+",                                    # tooltip
            self.activate_action ),
        );

        # GtkToggleActionEntry
        toggle_entries = (
          ( "Bold", gtk.STOCK_BOLD,                    # name, stock id
             "_Bold", "<control>B",                    # label, accelerator
            "Bold",                                    # tooltip
            self.activate_action,
            True ),                                    # is_active
        )

        # GtkRadioActionEntry
        color_entries = (
          ( "Red", None,                               # name, stock id
            "_Red", "<control><shift>R",               # label, accelerator
            "Blood", COLOR_RED ),                      # tooltip, value
          ( "Green", None,                             # name, stock id
            "_Green", "<control><shift>G",             # label, accelerator
            "Grass", COLOR_GREEN ),                    # tooltip, value
          ( "Blue", None,                              # name, stock id
            "_Blue", "<control><shift>B",              # label, accelerator
            "Sky", COLOR_BLUE ),                       # tooltip, value
        )

        # GtkRadioActionEntry
        shape_entries = (
          ( "Square", None,                            # name, stock id
            "_Square", "<control><shift>S",            # label, accelerator
            "Square",  SHAPE_SQUARE ),                 # tooltip, value
          ( "Rectangle", None,                         # name, stock id
            "_Rectangle", "<control><shift>R",         # label, accelerator
            "Rectangle", SHAPE_RECTANGLE ),            # tooltip, value
          ( "Oval", None,                              # name, stock id
            "_Oval", "<control><shift>O",              # label, accelerator
            "Egg", SHAPE_OVAL ),                       # tooltip, value
        )

        # Create the menubar and toolbar
        action_group = gtk.ActionGroup("AppWindowActions")
        action_group.add_actions(entries)
        action_group.add_toggle_actions(toggle_entries)
        action_group.add_radio_actions(color_entries, COLOR_RED, self.activate_radio_action)
        action_group.add_radio_actions(shape_entries, SHAPE_OVAL, self.activate_radio_action)

        return action_group

    def activate_about(self, action):
        dialog = gtk.AboutDialog()
        dialog.set_name("PyGTK Demo")
        dialog.set_copyright("\302\251 Copyright 200x the PyGTK Team")
        dialog.set_website("http://www.pygtk.org./")
        ## Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def activate_action(self, action):
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
            'You activated action: "%s" of type "%s"' % (action.get_name(), type(action)))
        # Close dialog on user response
        dialog.connect ("response", lambda d, r: d.destroy())
        dialog.show()

    def activate_radio_action(self, action, current):
        active = current.get_active()
        value = current.get_current_value()

        if active:
            dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE,
                "You activated radio action: \"%s\" of type \"%s\".\nCurrent value: %d" %
                (current.get_name(), type(current), value))

            # Close dialog on user response
            dialog.connect("response", lambda d, r: d.destroy())
            dialog.show()

    # In the GL example this doesn't get called because we've yanked
    # out the text buffer.  This is left it to show how to access
    # the status bar.  It's useful information to have.
    def update_statusbar(self, buffer):
        # clear any previous message, underflow is allowed
        self.statusbar.pop(0)
        count = buffer.get_char_count()
        iter = buffer.get_iter_at_mark(buffer.get_insert())
        row = iter.get_line()
        col = iter.get_line_offset()
        self.statusbar.push(0,
        'Cursor at row %d column %d - %d chars in document' % (row, col, count))

    def update_resize_grip(self, widget, event):
        mask = gtk.gdk.WINDOW_STATE_MAXIMIZED | gtk.gdk.WINDOW_STATE_FULLSCREEN
        if (event.changed_mask & mask):
            self.statusbar.set_has_resize_grip(not (event.new_window_state & mask))

def main():
    print "Press <ESC> to exit demo"
    ApplicationMainWindowDemo()
    gtk.main()

if __name__ == '__main__':
    main()
