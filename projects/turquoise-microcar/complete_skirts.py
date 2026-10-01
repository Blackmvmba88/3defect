"""Complete the four lower valance panels without rebuilding the vehicle."""
import bpy, bmesh, math

def complete_skirts():
    collection=bpy.data.collections['MICROCAR • editable components']
    for o in list(collection.objects):
        if o.name.startswith('Skirt • '):bpy.data.objects.remove(o,do_unlink=True)
    paint=bpy.data.materials['Turquoise clearcoat'];dark=bpy.data.materials['Deep turquoise trim']
    result=[]
    def panel(name,rows):
        verts=[p for row in rows for p in row];n=len(rows[0]);faces=[]
        for r in range(len(rows)-1):
            for i in range(n-1):faces.append((r*n+i,r*n+i+1,(r+1)*n+i+1,(r+1)*n+i))
        me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
        o=bpy.data.objects.new('Skirt • '+name,me);collection.objects.link(o);me.materials.append(paint)
        for f in me.polygons:f.use_smooth=True
        s=o.modifiers.new('Formed panel thickness','SOLIDIFY');s.thickness=.025
        b=o.modifiers.new('Soft perimeter edges','BEVEL');b.width=.012;b.segments=3
        o['role']='lower_body_skirt';result.append(o.name)
    for sign,label in [(-1,'left rocker'),(1,'right rocker')]:
        xs=[-.38+i*.76/24 for i in range(25)];rows=[]
        for z,y in [(.68,.846),(.60,.88),(.47,.90),(.425,.86),(.45,.79)]:
            rows.append([(x,sign*(y+.018*math.sin(math.pi*(x+.38)/.76)),z+.012*math.cos(math.pi*x/.76)) for x in xs])
        panel(label,rows)
    for sign,label in [(-1,'front valance'),(1,'rear valance')]:
        rows=[]
        for z,x in [(.73,1.42),(.65,1.48),(.53,1.475),(.445,1.43),(.46,1.35)]:
            row=[]
            for i in range(41):
                t=-1+2*i/40;y=.67*t;bow=.06*abs(t)**6
                row.append((sign*(x-bow),y,z+.028*abs(t)**4))
            rows.append(row)
        panel(label,rows)
    # Keep the user's four-face construction as an editable source; hide only
    # the overlapping patch now that complete manufactured panels replace it.
    old=bpy.data.objects.get('Lower skirt • user geometry retained')
    if old:
        backup=bpy.data.collections['USER_EDITS • preserved']
        for c in list(old.users_collection):c.objects.unlink(old)
        backup.objects.link(old)
    return {'lower_skirts':result,'skirt_count':len(result),'bilateral_rockers':True,'front_and_rear_valances':True}

if __name__=='__main__':
    import json,sys
    from pathlib import Path
    root=Path(__file__).resolve().parent
    bpy.ops.wm.open_mainfile(filepath=str(root/'Turquoise_Microcar.blend'))
    if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
    report=complete_skirts();p=root/'validation.json';data=json.loads(p.read_text());data.update(report);data['components']=len(bpy.data.collections['MICROCAR • editable components'].objects);p.write_text(json.dumps(data,indent=2))
    assert report['skirt_count']==4
    bpy.ops.wm.save_as_mainfile(filepath=str(root/'Turquoise_Microcar.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in bpy.data.collections['MICROCAR • editable components'].objects:o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(root/'Turquoise_Microcar.glb'),use_selection=True,export_apply=True)
    s=bpy.context.scene;s.cycles.samples=48;s.render.filepath=str(root/'Turquoise_Microcar.png');bpy.ops.render.render(write_still=True)
    print('SKIRTS_VALID',report)
