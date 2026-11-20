package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

import com.schoolrde.schoolservice.dao.repository.EventRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.schoolrde.schoolservice.entity.EventEntity;
import com.schoolrde.schoolservice.util.JsonUtility;

@Repository
public class EventDaoImpl implements EventDao{

    private static final Logger LOGGER = LoggerFactory.getLogger(EventDaoImpl.class);

    private final EventRepository eventRepository;

    public EventDaoImpl(EventRepository eventRepository){
        this.eventRepository=eventRepository;
    }

    @Override
    public List<EventEntity> findEventBySchoolId(Integer schoolId){
        LOGGER.info("Quering event from database with schoolId : {}", schoolId);
        return eventRepository.findBySchoolId(schoolId);
    }

    @Override
    public Optional<EventEntity> findEventById(Integer id){
        LOGGER.info("Quering event from database with id : {}", id);
        return eventRepository.findById(id);
    }

    @Override
    public EventEntity saveEvent(EventEntity eventEntity){
        LOGGER.info("event to be saved into DB : {}", JsonUtility.toJson(eventEntity));
        EventEntity savedEventEntity=eventRepository.save(eventEntity);
        LOGGER.info("event saved successfully : {}", JsonUtility.toJson(savedEventEntity));
        return savedEventEntity;
    }

}
