import ROOT as r
from array import array
from tqdm import tqdm

def convert_lhe(fname_in, fname_out="events.root"):

    f1 = r.TFile(fname_out, "recreate")
    t1 = r.TTree("t","t")

    pdgid = r.std.vector(int)()
    status = r.std.vector(int)()
    parent1 = r.std.vector(int)()
    parent2 = r.std.vector(int)()
    color1 = r.std.vector(int)()
    color2 = r.std.vector(int)()
    mass = r.std.vector(float)()
    spin = r.std.vector(float)()
    p4s = r.std.vector(r.TLorentzVector)()

    t1._pdgid   = pdgid    
    t1._status  = status 
    t1._parent1 = parent1
    t1._parent2 = parent2
    t1._color1  = color1 
    t1._color2  = color2 
    t1._mass    = mass  
    t1._spin    = spin  
    t1._p4      = p4s  

    p4 = r.TLorentzVector(1,1,0,5)

    t1.Branch("id", pdgid)
    t1.Branch("status", status)
    t1.Branch("parent1", parent1)
    t1.Branch("parent2", parent2)
    t1.Branch("color1", color1)
    t1.Branch("color2", color2)
    t1.Branch("mass", mass)
    t1.Branch("spin", spin)
    t1.Branch("p4", p4s)

    event = ""
    in_event = False
    with open(fname_in, "r") as fhin:
        iline = 0
        for line in tqdm(fhin):

            if in_event and line.startswith("<"):
                in_event = False

                particle_lines = event.splitlines()[1:]

                pdgid.clear()
                status.clear()
                parent1.clear()
                parent2.clear()
                color1.clear()
                color2.clear()
                mass.clear()
                spin.clear()
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

                    pdgid.push_back(evt_pdgid)
                    status.push_back(evt_status)
                    parent1.push_back(evt_parent1)
                    parent2.push_back(evt_parent2)
                    color1.push_back(evt_color1)
                    color2.push_back(evt_color2)
                    mass.push_back(evt_mass)
                    spin.push_back(evt_spin)
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
