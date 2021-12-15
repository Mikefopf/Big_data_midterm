UPDATE db.boardingdata
SET TicketNumber = NULL
WHERE TicketNumber = 'NaN';
UPDATE db.boardingdata
SET BookingCode = NULL
WHERE BookingCode = 'NaN';
UPDATE db.sirenaexport
SET TicketNumber = NULL
WHERE TicketNumber = 'NaN';
UPDATE db.sirenaexport
SET BookingCode = NULL
WHERE BookingCode = 'NaN';

SELECT COALESCE(t.ArrivalCity, ff.ArrivalCity)               AS ArrivalCity,
       BaggageState,
       BookingCode,
       COALESCE(t.CodeShare, ff.CodeShare)                   AS CodeShare,
       COALESCE(t.DepartureDate, ff.DepartureDate)           AS DepartureDate,
       DepartureTime,
       COALESCE(t.FlightNumber, ff.FlightNumber)             AS FlightNumber,
       PassengerBirthDate,
       PassengerDocument,
       COALESCE(t.PassengerFirstName, ff.PassengerFirstName) AS PassengerFirstName,
       COALESCE(t.PassengerLastName, ff.PassengerLastName)   AS PassengerLastName,
       PassengerSecondName,
       COALESCE(t.PassengerSex, ff.PassengerSex)             AS PassengerSex,
       TicketNumber,
       AgentInfo,
       COALESCE(t.ArrivalAirport, ff.ArrivalAirport)         AS ArrivalAirport,
       ArrivalDate,
       ArrivalTime,
       BaggageCount,
       COALESCE(t.DepartureAirport, ff.DepartureAirport)     AS DepartureAirport,
       Fare,
       Meal,
       PassengerAdditionalInfo,
       PassengerClass,
       ArrivalCountry,
       DepartureCity,
       DepartureCountry,
       PassengerNickName
FROM (SELECT ArrivalCity,
             BaggageState,
             COALESCE(bd.BookingCode, se.BookingCode)                 BookingCode,
             COALESCE(bd.CodeShare, se.CodeShare)                     CodeShare,
             COALESCE(bd.DepartureDate, se.DepartureDate)             DepartureDate,
             COALESCE(bd.DepartureTime, se.DepartureTime)             DepartureTime,
             COALESCE(bd.FlightNumber, se.FlightNumber)               FlightNumber,
             COALESCE(bd.PassengerBirthDate, se.PassengerBirthDate)   PassengerBirthDate,
             COALESCE(bd.PassengerDocument, se.PassengerDocument)     PassengerDocument,
             COALESCE(bd.PassengerFirstName, se.PassengerFirstName)   PassengerFirstName,
             COALESCE(bd.PassengerLastName, se.PassengerLastName)     PassengerLastName,
             COALESCE(bd.PassengerSecondName, se.PassengerSecondName) PassengerSecondName,
             PassengerSex,
             COALESCE(bd.TicketNumber, se.TicketNumber)               TicketNumber,
             AgentInfo,
             ArrivalAirport,
             ArrivalDate,
             ArrivalTime,
             BaggageCount,
             DepartureAirport,
             Fare,
             Meal,
             PassengerAdditionalInfo,
             PassengerClass
      FROM BoardingData bd
               LEFT JOIN SirenaExport se ON
                  bd.FlightNumber = se.FlightNumber AND
                  bd.DepartureDate = se.DepartureDate AND
                  bd.PassengerFirstName = se.PassengerFirstName AND
                  bd.PassengerLastName = se.PassengerLastName
      UNION
      SELECT ArrivalCity,
             BaggageState,
             COALESCE(bd.BookingCode, se.BookingCode)                 BookingCode,
             COALESCE(bd.CodeShare, se.CodeShare)                     CodeShare,
             COALESCE(bd.DepartureDate, se.DepartureDate)             DepartureDate,
             COALESCE(bd.DepartureTime, se.DepartureTime)             DepartureTime,
             COALESCE(bd.FlightNumber, se.FlightNumber)               FlightNumber,
             COALESCE(bd.PassengerBirthDate, se.PassengerBirthDate)   PassengerBirthDate,
             COALESCE(bd.PassengerDocument, se.PassengerDocument)     PassengerDocument,
             COALESCE(bd.PassengerFirstName, se.PassengerFirstName)   PassengerFirstName,
             COALESCE(bd.PassengerLastName, se.PassengerLastName)     PassengerLastName,
             COALESCE(bd.PassengerSecondName, se.PassengerSecondName) PassengerSecondName,
             PassengerSex,
             COALESCE(bd.TicketNumber, se.TicketNumber)               TicketNumber,
             AgentInfo,
             ArrivalAirport,
             ArrivalDate,
             ArrivalTime,
             BaggageCount,
             DepartureAirport,
             Fare,
             Meal,
             PassengerAdditionalInfo,
             PassengerClass
      FROM BoardingData bd
               RIGHT JOIN SirenaExport se
                          ON
                                      bd.FlightNumber = se.FlightNumber AND
                                      bd.DepartureDate = se.DepartureDate AND
                                      bd.PassengerFirstName = se.PassengerFirstName AND
                                      bd.PassengerLastName = se.PassengerLastName) t
         LEFT JOIN db.frequentflyerforumflights ff ON t.FlightNumber = ff.FlightNumber AND
                                                      t.DepartureDate = ff.DepartureDate AND
                                                      t.PassengerFirstName = ff.PassengerFirstName AND
                                                      t.PassengerLastName = ff.PassengerLastName
ORDER BY DepartureDate, FlightNumber, PassengerLastName, PassengerFirstName;
