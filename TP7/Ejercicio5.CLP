(defrule leer-estado
	=>
	(printout t "Seleccione el estado de la enfermedad (incipiente/avanzado/terminal): ")
	(assert (estado(read)))
)

(defrule leer-concentracion
	(estado ?)
	=>
	(printout t "Concentracion de la sustancia (Numero): ")
	(assert (concentracion(read)))
)

(defrule leer-dosis
	(estado ?)
	=>
	(printout t "Numero de dosis (Numero): ")
	(assert (ndosis(read)))
)

(defrule leer-condicion
	(estado ?)
	=>
	(printout t "Condicion fisica(debil/fuerte): ")
	(assert (condicion(read)))
)

(defrule estado-avanzado
	(estado ?c)
	=>
	(if (eq ?c avanzado)
	then
		(assert (curar si))
	)
)

(defrule estado-incipiente-ndosis
  (estado ?c)
  (ndosis ?h)
  =>
  (if (eq ?c incipiente)
  then
    (if (> ?h 80.35)
    then
      (assert (curar no))
    else
      (assert (curar si))
    )
  )
)


(defrule estado-terminal-condicion
	(estado ?c)
	(condicion ?v)
	=>
	(if (eq ?c terminal)
	then
		(if (eq ?v fuerte)
		then
			(assert (curar no))
		else
			(assert (curar si))
		)
	)
)

(defrule jugamos
	(curar ?j)
	(estado ?)
	(ndosis ?)
	(condicion ?)
	=>
	(printout t ?j " se cura.")
) 