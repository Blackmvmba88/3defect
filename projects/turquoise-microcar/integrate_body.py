"""Build a single connected upper shell with quad inset rings and glazing."""
import bpy, bmesh, math
from mathutils import Vector

def integrate_shell():
    scene=bpy.context.scene
    backup=bpy.data.collections.get('USER_EDITS • preserved')
    if backup is None:
        backup=bpy.data.collections.new('USER_EDITS • preserved');scene.collection.children.link(backup)
    backup.hide_render=True;backup.hide_viewport=True
    for name in ['Cube','Rounded lower body.001']:
        o=bpy.data.objects.get(name)
        if o:
            saved=o.copy();saved.data=o.data.copy();saved.name='Original user edit • '+name;backup.objects.link(saved)
    # Replace the opaque test cage and detached painted window tubes.
    remove=['Upper chassis • one piece with inset window frames','Integrated domed roof','Integrated rounded roof','Cube','Panoramic windshield','Rear hatch glass','Rear hatch frame','Rear hatch seal','Windshield painted surround','Windshield gasket','Windshield brightwork']
    for o in list(bpy.data.objects):
        if o.name in remove or any(o.name.startswith(p) for p in ['Inset glass • ','Inset window gasket ','Inset window chrome lip ','Door glass ','Quarter glass ','Door painted frame ','Quarter painted frame ','Door weather seal ','Quarter weather seal ','Door chrome reveal ','Quarter chrome reveal ']):
            bpy.data.objects.remove(o,do_unlink=True)
    car=bpy.data.collections.get('MICROCAR • editable components')
    paint=bpy.data.materials['Turquoise clearcoat'];glass=bpy.data.materials['Tinted optical glass'];seal=bpy.data.materials['Rubber window seals'];chrome=bpy.data.materials['Polished silver']
    verts=[];faces=[];roof_coords=[];windows=[];N=64
    def mapped(wall,u,v):
        z=1.4+1.22*v;front=-1.05+.36*v;rear=1.30-.32*v;width=.84-.14*v
        if wall=='front':return Vector((front,(2*u-1)*width,z))
        if wall=='rear':return Vector((rear,(1-2*u)*width,z))
        sign=-1 if wall=='left' else 1
        return Vector((front+(rear-front)*u,sign*width,z))
    def inward(wall):return Vector((1,0,0)) if wall=='front' else Vector((-1,0,0)) if wall=='rear' else Vector((0,1,0)) if wall=='left' else Vector((0,-1,0))
    patches=[('front',0,1),('rear',0,1),('left',0,.55),('left',.55,1),('right',0,.55),('right',.55,1)]
    for idx,(wall,start,end) in enumerate(patches):
        rings=[]
        for ring in range(3):
            indices=[];coords=[]
            for i in range(N):
                a=math.tau*i/N;co=math.cos(a);si=math.sin(a)
                if ring==0:
                    d=max(abs(co),abs(si));u=.5+.5*co/d;v=.5+.5*si/d
                else:
                    # Rounded inset border, followed by a recessed glass seat.
                    u=.5+.44*math.copysign(abs(co)**.38,co);v=.53+.425*math.copysign(abs(si)**.38,si)
                p=mapped(wall,start+(end-start)*u,v)
                if ring==2:p+=inward(wall)*.023
                indices.append(len(verts));verts.append(tuple(p));coords.append(tuple(p))
                if ring==0 and abs(v-1)<1e-6:roof_coords.append(tuple(p))
            rings.append(indices)
            if ring==2:windows.append((wall,idx,coords))
        for j in range(2):
            for i in range(N):faces.append((rings[j][i],rings[j][(i+1)%N],rings[j+1][(i+1)%N],rings[j+1][i]))
    # Loft the roof directly from the same boundary vertices as the window walls.
    unique={tuple(round(x,6) for x in p):p for p in roof_coords}
    boundary=sorted(unique.values(),key=lambda p:math.atan2(p[1],p[0]-.145))
    previous=[]
    for p in boundary:previous.append(len(verts));verts.append(p)
    for scale,z in [(.97,2.67),(.84,2.74),(.57,2.79),(.27,2.815),(.035,2.82)]:
        current=[]
        for p in boundary:current.append(len(verts));verts.append((.145+(p[0]-.145)*scale,p[1]*scale,z))
        for i in range(len(boundary)):faces.append((previous[i],previous[(i+1)%len(boundary)],current[(i+1)%len(boundary)],current[i]))
        previous=current
    faces.append(tuple(previous))
    me=bpy.data.meshes.new('Upper body • connected quad inset shell');me.from_pydata(verts,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00002);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new('Upper chassis • one piece with inset window frames',me);car.objects.link(o);me.materials.append(paint)
    for f in me.polygons:f.use_smooth=True
    sub=o.modifiers.new('Continuous body curvature','SUBSURF');sub.levels=2;sub.render_levels=2
    solid=o.modifiers.new('Body shell thickness 18 mm','SOLIDIFY');solid.thickness=.018;solid.offset=-1
    bevel=o.modifiers.new('Soft body corners','BEVEL');bevel.width=.018;bevel.segments=3
    o['construction']='One connected surface, six inset window openings, recessed glazing seats, integral domed roof'
    def trim(name,points,r,mat):
        c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('POLY');s.points.add(len(points)-1)
        for q,p in zip(s.points,points):q.co=(*p,1)
        s.use_cyclic_u=True;ob=bpy.data.objects.new(name,c);car.objects.link(ob);ob.data.materials.append(mat)
    for wall,idx,pts in windows:
        n=inward(wall);points=[tuple(Vector(p)+n*.004) for p in pts]
        m=bpy.data.meshes.new('Inset glass '+str(idx));m.from_pydata(points,[],[tuple(range(N))]);m.update();ob=bpy.data.objects.new('Inset glass • '+wall+' '+str(idx),m);car.objects.link(ob);m.materials.append(glass);mod=ob.modifiers.new('Optical thickness 8 mm','SOLIDIFY');mod.thickness=.008
        trim('Inset window gasket '+str(idx),pts,.012,seal);trim('Inset window chrome lip '+str(idx),[tuple(Vector(p)-n*.01) for p in pts],.005,chrome)
    skirt=bpy.data.objects.get('Rounded lower body.001') or bpy.data.objects.get('Lower skirt • user geometry retained')
    if skirt:
        skirt.name='Lower skirt • user geometry retained';skirt.data.materials.clear();skirt.data.materials.append(paint)
        for p in skirt.data.polygons:p.material_index=0
        if not skirt.get('panel_offset_applied',False):
            for v in skirt.data.vertices:
                if abs(v.co.y)>.5:v.co.y+=math.copysign(.009,v.co.y)
            skirt['panel_offset_applied']=True
        if not any(m.type=='SOLIDIFY' for m in skirt.modifiers):s=skirt.modifiers.new('Skirt panel thickness','SOLIDIFY');s.thickness=.014
    # Topology check: one connected shell, six glazing openings plus the lower edge.
    bm=bmesh.new();bm.from_mesh(me);pending=set(bm.verts);components=0
    while pending:
        components+=1;stack=[pending.pop()]
        while stack:
            v=stack.pop()
            for e in v.link_edges:
                w=e.other_vert(v)
                if w in pending:pending.remove(w);stack.append(w)
    edges=sum(e.is_boundary for e in bm.edges);bm.free();assert components==1,components
    return {'upper_shell_connected_components':components,'inset_windows':len(windows),'upper_shell_vertices':len(me.vertices),'upper_shell_boundary_edges_before_thickness':edges,'user_skirt_retained':bool(skirt)}
