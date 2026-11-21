package com.schoolrde.schoolservice.dao.bussiness;

import java.util.List;
import java.util.Optional;

import com.schoolrde.schoolservice.entity.SourceEntity;

public interface SourceDao{
	
    SourceEntity saveSource(SourceEntity source);

    List<SourceEntity> findSourceBySchoolId(Integer schoolId);

    Optional<SourceEntity> findSourceById(Integer id);

}
