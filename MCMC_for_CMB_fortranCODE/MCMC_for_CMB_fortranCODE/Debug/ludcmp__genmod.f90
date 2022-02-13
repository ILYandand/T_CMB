        !COMPILER-GENERATED INTERFACE MODULE: Wed Feb  9 20:35:25 2022
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE LUDCMP__genmod
          INTERFACE 
            SUBROUTINE LUDCMP(A,N,NP,INDX,D)
              INTEGER(KIND=4) :: NP
              INTEGER(KIND=4) :: N
              REAL(KIND=8) :: A(NP,NP)
              INTEGER(KIND=4) :: INDX(N)
              REAL(KIND=8) :: D
            END SUBROUTINE LUDCMP
          END INTERFACE 
        END MODULE LUDCMP__genmod
