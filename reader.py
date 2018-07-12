import ROOT as r
from array import array
from tqdm import tqdm

def convert_lhe(fname_in, fname_out="events.root"):

    f1 = r.TFile(fname_out, "recreate")
    t1 = r.TTree("t","t")
    pdgid = array( 'i', [ 0,0,0,0,0 ] )
    status = array( 'i', [ 0,0,0,0,0 ] )
    parent1 = array( 'i', [ 0,0,0,0,0 ] )
    parent2 = array( 'i', [ 0,0,0,0,0 ] )
    color1 = array( 'i', [ 0,0,0,0,0 ] )
    color2 = array( 'i', [ 0,0,0,0,0 ] )
    mass = array( 'd', [ 0,0,0,0,0 ] )
    spin = array( 'd', [ 0,0,0,0,0 ] )
    p4s = r.std.vector(r.TLorentzVector)()
    t1._p4 = p4s
    p4 = r.TLorentzVector(1,1,0,5)
    t1.Branch("id",pdgid, "id[5]/I")
    t1.Branch("status",status, "status[5]/I")
    t1.Branch("parent1",parent1, "parent1[5]/I")
    t1.Branch("parent2",parent2, "parent2[5]/I")
    t1.Branch("color1",color1, "color1[5]/I")
    t1.Branch("color2",color2, "color2[5]/I")
    t1.Branch("mass",mass, "mass[5]/F")
    t1.Branch("spin",spin, "spin[5]/F")
    t1.Branch("p4",p4s)

    event = ""
    in_event = False
    with open(fname_in, "r") as fhin:
        iline = 0
        for line in tqdm(fhin):

            if in_event and line.startswith("<"):
                in_event = False

                particle_lines = event.splitlines()[1:]
                p4s.clear()
                for index,particle_line in enumerate(particle_lines):
                    parts = particle_line.split()
                    evt_pdgid = int(parts[0])
                    evt_status = int(parts[1])
                    evt_parent1 = int(parts[2])
                    evt_parent2 = int(parts[3])
                    evt_color1 = int(parts[4])
                    evt_color2 = int(parts[5])
                    evt_px, evt_py, evt_pz, evt_e = map(float,parts[6:10])
                    evt_mass = float(parts[10])
                    evt_spin = float(parts[11])
                    p4.SetPxPyPzE(evt_px, evt_py, evt_pz, evt_e)
                    pdgid[index] = evt_pdgid
                    status[index] = evt_status
                    parent1[index] = evt_parent1
                    parent2[index] = evt_parent2
                    color1[index] = evt_color1
                    color2[index] = evt_color2
                    mass[index] = evt_mass
                    spin[index] = evt_spin
                    p4s.push_back(p4)

                t1.Fill()

                event = ""

            if in_event:
                event += line

            if line.startswith("<event>"):
                in_event = True

    t1.Print()
    t1.Write()
    f1.Close()

if __name__ == "__main__":

    convert_lhe("/Users/fgolf/sw/madgraph/MG5_aMC_v2_6_1/ttg_lo_ggonly_test/Events/run_01/tmp/unweighted_events.lhe")
