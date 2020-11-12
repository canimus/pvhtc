let challenger: string
type fullStackDataScientist = skills.PYTHON | skills.TYPESCRIPT
interface DataScientist {
    fullstack: fullStackDataScientist
}
enum skills {
    TYPESCRIPT,
    PYTHON,
    BASH
}

let herminio: DataScientist
herminio.fullstack = 0

challenger = "Herminio Vazquez"
console.log(herminio)