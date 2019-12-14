tinp = """180 ORE => 9 DQFL
3 HGCR, 9 TKRT => 8 ZBLC
1 MZQLG, 12 RPLCK, 8 PDTP => 8 VCFX
3 ZBLC, 19 VFZX => 1 SJQL
1 CRPGK => 4 TPRT
7 HGCR, 4 TGCW, 1 VFZX => 9 JBPHS
8 GJHX => 4 NSDBV
1 VFTG => 2 QNWD
1 WDKW, 2 DWRH, 6 VNMV, 2 HFHL, 55 GJHX, 4 NSDBV, 15 KLJMS, 17 KZDJ => 1 FUEL
2 JHSJ, 15 JNWJ, 1 ZMFXQ => 4 GVRK
1 PJFBD => 3 MZQLG
1 SJQL, 11 LPVWN => 9 DLZS
3 PRMJ, 2 XNWV => 6 JHSJ
4 SJQL => 8 PJFBD
14 QNWD => 6 STHQ
5 CNLFV, 2 VFTG => 9 XNWV
17 LWNKB, 6 KBWF, 3 PLSCB => 8 KZDJ
6 LHWZQ, 5 LWNKB => 3 ZDWX
5 RPLCK, 2 LPVWN => 8 ZMFXQ
1 QNWD, 2 TKRT => 3 CRPGK
1 JBPHS, 1 XNWV => 6 TLRST
21 ZDWX, 3 FZDP, 4 CRPGK => 6 PDTP
1 JCVP => 1 WXDVT
2 CRPGK => 9 FGVL
4 DQFL, 2 VNMV => 1 HGCR
2 GVRK, 2 VCFX, 3 PJFBD, 1 PLSCB, 23 FZDP, 22 PCSM, 1 JLVQ => 6 HFHL
1 CRPGK, 5 PJFBD, 4 XTCP => 8 PLSCB
1 HTZW, 17 FGVL => 3 LHWZQ
2 KBWF => 4 DQKLC
2 LHWZQ => 2 PRMJ
2 DLZS, 2 VCFX, 15 PDTP, 14 ZDWX, 35 NBZC, 20 JVMF, 1 BGWMS => 3 DWRH
2 TKVCX, 6 RPLCK, 2 HTZW => 4 XTCP
8 CNLFV, 1 NRSD, 1 VFTG => 9 VFZX
1 TLRST => 4 WDKW
9 VFCZG => 7 GJHX
4 FZDP => 8 JLVQ
2 ZMFXQ, 2 STHQ => 6 QDZB
2 SJQL, 8 ZDWX, 6 LPRL, 6 WXDVT, 1 TPRT, 1 JNWJ => 8 KLJMS
6 JBPHS, 2 ZBLC => 6 HTZW
1 PDTP, 2 LHWZQ => 8 JNWJ
8 ZBLC => 7 TKVCX
2 WDKW, 31 QDZB => 4 PCSM
15 GJHX, 5 TKVCX => 7 FZDP
15 SJQL, 3 PRMJ => 4 JCVP
31 CNLFV => 1 TGCW
1 TLRST, 2 WDKW => 9 KBWF
102 ORE => 7 VNMV
103 ORE => 5 CNLFV
163 ORE => 2 VFTG
5 NRSD, 1 STHQ => 3 VFCZG
16 LPVWN, 13 KBWF => 2 BGWMS
5 BGWMS, 11 SJQL, 9 FZDP => 6 NBZC
175 ORE => 7 NRSD
5 HTZW => 4 LPVWN
4 PRMJ => 7 JVMF
6 PCSM, 8 DQKLC => 7 LPRL
2 CNLFV => 7 TKRT
3 FZDP => 3 LWNKB
1 HTZW => 4 RPLCK"""

def inp_decode(x):
    reactions = {}
    for line in x.split('\n'):
        in_, out_ = map(str.strip, line.split("=>"))
        def parse_elem(x):
            v, n = x.split(" ")
            return (int(v), n)
        in_ = list(map(parse_elem, map(str.strip, in_.split(","))))
        out_ = parse_elem(out_)
        reactions[out_[1]] = (in_, out_)
    return reactions

reactions = inp_decode(tinp)

def calculate(nr):
    needed = {"FUEL": nr}
    available = {}
    while len(needed) != 1 or not "ORE" in needed:
        needednow = []
        for n, v in needed.items():
            if n == "ORE" or v == 0:
                continue
            start = reactions[n]
            if n in available:
                if needed[n] > available[n]:
                    needed[n] -= available[n]
                    available[n] -= available[n]
                else:
                    available[n] -= needed[n]
                    needed[n] = 0
                    continue
            needednow.append(n)
        fac = {}
        for n in needednow:
            start = reactions[n]
            producable = start[1][0]
            if needed[n] <= producable:
                fac[n] = 1
            else:
                fac[n] = needed[n] // producable
                if needed[n] % producable != 0:
                    fac[n] += 1
        for n in needednow:
            start = reactions[n]
            for elem in start[0]:
                amount = elem[0] * fac[n]
                if elem[1] in needed:
                    needed[elem[1]] += amount
                else:
                    needed[elem[1]] = amount
                amount - needed[n]
            needed[n] -= start[1][0] * fac[n]
            if needed[n] < 0:
                available[n] = -needed[n]
                needed[n] = 0
            else:
                needed[n] = needed[n]

        for d in list(needed.keys()):
            if needed[d] == 0:
                del needed[d]

    return needed["ORE"]
def main():
    print(calculate(1))
    nr = 1
    step = 10000000
    while step > 0:
        while calculate(nr) < 1000000000000:
            nr += step
        nr -= step
        step = step // 10
    print(nr)

if __name__ == "__main__":
    main()
